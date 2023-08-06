#!/usr/bin/env python3
import multiprocessing
from optparse import OptionParser
import os,sys
import json
import logging
import configparser
import socket

import docker
from sty import fg, bg
import ia
from ia.gaius.genome_info import Genome

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
datefmt='%Y-%m-%d:%H:%M:%S')
logger = logging.getLogger("spawn_agent")
logger.setLevel(level=logging.INFO)

ASSETS = {'network': {},
          'agent': None,
          'genome': None,
          'interfaces': {},
          'cp-containers': {},
          'mp-containers': {},
          'applications': {} ## These are connected containers as applications. Ex. JIA notebooks.
          }

def retrieve_genome(genome_file):
    logger.debug(f'{genome_file = }')
    
    # if provided filepath, attempt to open genome
    if os.path.exists(genome_file):
        with open(genome_file, 'r') as f:

            # read data into genome_json
            genome_json = f.read()
            _g = json.loads(genome_json)
            # convert json to python dictionary

    # otherwise try to load genome from string
    else:
        try:
            genome_json = genome_file
            _g = json.loads(genome_file)
        except json.decoder.JSONDecodeError:
            logger.critical(f'Failed to retreive genome, {genome_file=}')
            sys.exit(1)

    # remove description fields from genome
    _g['description'] = 'cleared description'
    for d in _g['elements']['nodes']:
        if 'description' in d['data'].keys():
            logger.debug(f"Removing: {d['data']['description']}")
            d['data']['description'] = ''

    return Genome(_g)

def parse_genome(genome):

    targets_map = {} ## values are target IDs for each key
    sources_map = {} ## values are source IDs of each key

    if 'edges' not in genome.topology['elements']:
        logger.warning("No connections.")
    else:
        for edge in genome.topology['elements']['edges']:
            d = edge['data']
            if d['source'] not in targets_map:
                if d['source'].startswith("action"):
                    continue
                targets_map[d['source']] = [d['target']]
            else:
                if d['source'].startswith("action"):
                    continue
                targets_map[d['source']].append(d['target'])
            if d['target'] not in sources_map:
                if d['target'].startswith("action"):
                    continue
                sources_map[d['target']] = [d['source']]
            else:
                if d['target'].startswith("action"):
                    continue
                sources_map[d['target']].append(d['source'])

    targets_map = eval( f"{targets_map}".replace(", 'P1_ID': ['action1_ID', 'action2_ID']", ""))

    as_inputs = {pid: [] for pid in genome.primitives.keys() }
    is_input = []

    for pid, p in genome.primitives.items():
        logger.debug(f"{pid} ({p['name']}):")
        logger.debug(f"    {p['sources']}")
        if p['sources'] == ['observables']:
            as_inputs[pid] = []
        else:
            for mid in p['manipulatives']:
                if mid.startswith("action"):
                    continue
                logger.debug(f"   {mid} {genome.manipulatives[mid]['name']} {genome.manipulatives[mid]['genes']['sources']['value']}")
                if genome.manipulatives[mid]['genes']['sources']['value'] == ['observables']:
                    as_inputs[pid].append(mid)
                    is_input.append(mid)

    logger.debug(f'{as_inputs=}')
    logger.debug(f'{is_input=}')


    logger.debug(f'{targets_map=}')
    ## for any manipulative that is an observables (i.e. in is_input list),
    ## remove that manipulative from targets of other manipulatives:
    for _id, targets in targets_map.items():
        for mid in is_input:
            logger.debug(f"Need to pop: {mid} from {targets}")
            while mid in targets:
                logger.debug(f"popping...{mid} from {_id}")
                targets_map[_id].pop(targets.index(mid))

    # print("PROCESSING OBSERVABLES MANIPULATIVES")
    for mid, x in genome.manipulatives.items():
        if ['observables'] == x['genes']['sources']['value']:
            sources_map[mid] = [x['primitive']]


    logger.debug("sources_map:")
    for k,v in sources_map.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    <---{t}")

    logger.debug("targets_map:")
    for k,v in targets_map.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    --->{t}")

    logger.debug("as_inputs:")
    for k,v in as_inputs.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    --->({t})")

    return sources_map, targets_map, as_inputs

def check_container_conflicts(p_ids, running_container_names):
    docker_client = docker.from_env()
    logger.debug(f'checking container conflicts')
    for _id in p_ids:
        logger.debug(f'  -> {_id}')
        if _id in running_container_names:
            x = input(f"{bg.red}{fg.white} Conflicting containers! {_id} already exists.{bg.rs}{fg.rs} Okay to replace? Y/N: ")
            if x.lower() == 'y':
                c = docker_client.containers.get(_id)
                c.stop()
                c.remove()
            else:
                logger.debug(f"{bg.yellow}{fg.white} Aborting!{fg.rs}{bg.rs}")
                sys.exit()
    return

def find_available_ports():
    """Search all docker containers, looking for free ports to assign
    to GAIuS API, starting at port 8000 (unsecured) and 44300 (secured)

    Returns:
        dict: showing ports found
    """
    docker_client = docker.from_env()
    port_connects={}
    port_offset=0
    port_base = 8000
    port_limit = 8200
    port_list = []
    
    for each in docker_client.containers.list():
        for ports in each.ports.values():
            if ports is None:
                continue
            for port in ports:
                port_list.append(int(port['HostPort']))
    while port_base + port_offset < port_limit:
        if (port_base + port_offset not in port_list) and (44300 + port_offset not in port_list):
            port_connects={'80/tcp': port_base+port_offset, '443/tcp': 44300+port_offset}
            break;
        else:
            port_offset += 1

    if port_base + port_offset >= port_limit:
        logger.debug(f'failed to assign ports: reached port limit')
        sys.exit(1)
    return port_connects

def startit(genome_file, 
            BOTTLE_HOSTNAME=None,
            REGISTRY=None,
            VERSION=None,
            API_KEY=None,
            LOG_LEVEL=None,
            NETWORK=None,
            BIND_PORTS=None,
            user_id = None,
            agent_id = None):

    if user_id is None:
        raise Exception('no user id provided')
    if agent_id is None:
        raise Exception('no agent_id provided')

    docker_client = docker.from_env()
    container_extension = '-' + user_id + '-' +  agent_id

    genome = retrieve_genome(genome_file=genome_file)

    if not NETWORK:
        NETWORK="g2network"

    net_name = NETWORK + container_extension
    ## Does this network already exist?
    net_name_exists = False
    for n in docker_client.networks.list():
        if n.name == net_name:
            net_name_exists = True
            net = n
    if net_name_exists:
        logger.warning(f"error, {net_name} already exists!")
    else:
        net = docker_client.networks.create(net_name)
        logger.debug(f"{fg.green} Created {net.name} with id: {net.short_id} {fg.rs}")
    logger.debug(net_name)
    logger.debug(net)
    ASSETS['network'][net_name] = net
    
    sources_map, targets_map, as_inputs = parse_genome(genome)

    running_container_names = [c.name for c in docker_client.containers.list()]
    p_ids = list(genome.manipulative_map.keys() ) + list(genome.primitive_map.values()) + ['gaius-api']
    p_ids = [f'{_id}{container_extension}' for _id in p_ids]
    check_container_conflicts(p_ids, running_container_names)

    logger.debug("Starting Manipulative nodes...")
    for _id, m in genome.manipulative_map.items():
        if _id.startswith('action'): ## Needed for old testing topologies.
                continue
        manipulatives_genes = json.dumps(genome.manipulatives[_id])
        if _id in sources_map:
            sources = json.dumps(sources_map[_id])
        else:
            sources = json.dumps([])
        if _id in targets_map:
            targets = json.dumps(targets_map[_id])
        else:
            targets = json.dumps([])

        ASSETS['mp-containers'][_id] = docker_client.containers.run(
            name=_id + container_extension,
            image=f"{REGISTRY}manipulative-processor:{VERSION}",
            network=net_name,
            detach=True,
            init=True,
            hostname=_id,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                         'API_KEY': API_KEY,
                         'HOSTNAME': _id,
                         'MANIFEST': manipulatives_genes,
                         'SOURCES': sources,
                         'TARGETS': targets}
            )

    logger.debug("Starting Cognitive Processor nodes...")
    for p, _id in genome.primitive_map.items():
        primitive_genes = json.dumps(genome.primitives[_id])
        if _id in sources_map:
            sources = json.dumps(sources_map[_id])
        else:
            sources = json.dumps([])
        if _id in targets_map:
            targets = json.dumps(targets_map[_id])
        else:
            targets = json.dumps([])
        if _id in as_inputs:
            inputs = json.dumps(as_inputs[_id])
        else:
            inputs = json.dumps([])

        image=f"{REGISTRY}cognitive-processor:{VERSION}"
        logger.debug(f"using cognitive processor image {image}")
        ASSETS['cp-containers'][_id] = docker_client.containers.run(
            name=_id + container_extension,
            image=image,
            network=net_name,
            detach=True,
            init=True,
            hostname=_id,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                         'API_KEY': API_KEY,
                         'HOSTNAME': _id,
                         'MANIFEST': primitive_genes,
                         'SOURCES': sources,
                         'AS_INPUTS': inputs,
                         'TARGETS': targets}
            )

    logger.debug("Starting GAIuS-API interface node...")

    port_connects = {}
    if BIND_PORTS:
        port_connects = find_available_ports()
        
    ASSETS['interfaces']['gaius-api' + container_extension] = docker_client.containers.run(name='gaius-api' + container_extension,
            image=f"{REGISTRY}gaius-api:{VERSION}",
            network=net_name,
            detach=True,
            init=True,
            ports=port_connects,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                         'API_KEY': API_KEY,
                         'HOSTNAME': BOTTLE_HOSTNAME,
                         'GENOME': json.dumps(genome.topology),
                         'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION': "cpp"}
            )

    # print summary
    logger.info(f'{fg.green}GAIuS Agent started on docker network {fg.blue}{str(net_name)}{fg.rs}')
    if(BIND_PORTS):
        logger.info(f'{fg.green} Ports {fg.blue}{str(port_connects)}{fg.green} are exposed to the host{fg.rs}')
    else:
        logger.warning(f'{fg.green}Ports were not exposed for this agent. re-run command with {fg.blue}--bind-ports{fg.green} to expose ports{fg.rs}')
    return net_name, port_connects

def stopContainer(id):
    try:
        docker_client = docker.from_env()
        logger.info(f'''stopping container {id}''')
        c = docker_client.containers.get(id)
        c.stop()
        c.remove()
        logger.info(f'''container {id} removed{fg.rs}''')
    except:
        logger.debug(f'''{fg.red}container {id} did not exist... continuing{fg.rs}''')

def stopit(genome_file, user_id=None, agent_id=None):

    if user_id is None:
        raise Exception('no user id provided')
    if agent_id is None:
        raise Exception('no agent_id provided')

    container_extension = '-' + user_id + '-' +  agent_id
    docker_client = docker.from_env()

    genome = retrieve_genome(genome_file)

    ids = list(genome.primitive_map.values()) + list(genome.manipulative_map.keys())
    ids.append('gaius-api')

    ids = ['{0}{1}'.format(id, container_extension) for id in ids]
    multiPool = multiprocessing.Pool()
    multiPool.map(stopContainer, ids)

    try:
        logger.debug("pruning docker system")
        docker_client.containers.prune()
        docker_client.networks.prune()
    except:
        logger.warn("unable to prune docker")
        sys.exit(-1)

    return

def execute_agent(BOTTLE_HOSTNAME   = None,
                  REGISTRY            = 'registry.digitalocean.com/intelligent-artifacts',
                  VERSION             = 'latest',
                  API_KEY             = None,
                  LOG_LEVEL           = 'DEBUG',
                  NETWORK             = None,
                  BIND_PORTS          = True,
                  GENOME              = None,
                  AGENT_ID            = None,
                  USER_ID             = None,
                  KILL                = False
                  ):

    if GENOME is None:
        raise Exception('No genome provided')

    if not os.path.exists(f"{os.path.expanduser('~')}/.gaius"):
        os.mkdir(f"{os.path.expanduser('~')}/.gaius")

    if not API_KEY:
        API_KEY = 'ABCD-1234'

    if not NETWORK:
        NETWORK = 'g2network'

    configuration = {
                    'BOTTLE_HOSTNAME': BOTTLE_HOSTNAME,
                    'REGISTRY': REGISTRY,
                    'VERSION': VERSION,
                    'API_KEY': API_KEY,
                    'LOG_LEVEL': LOG_LEVEL,
                    'NETWORK': NETWORK,
                    'BIND_PORTS': BIND_PORTS,
                    'user_id' : USER_ID,
                    'agent_id' : AGENT_ID,
                    }

    genome_file = GENOME

    if KILL:
        stopit(genome_file, user_id=USER_ID, agent_id=AGENT_ID)
        return -1

    _, ports = startit(genome_file, **configuration)
    
    return ports

def start_agent(json_obj: dict):
    '''Start an agent from a genome passed as JSON

    fields => example:

        genome => json representation of genome
        user_id => test_user
        agent_id => agent1
        kill => False
        version => "latest"

    '''
    
    # required fields
    genome = json_obj['genome']
    user_id = json_obj['user_id']
    agent_id = json_obj['agent_id']
    kill = json_obj['kill']
    network = json_obj['network']
    
    # optional fields
    api_key = json_obj.get('api_key', "ABCD-1234")
    registry = json_obj.get('registry', 'registry.digitalocean.com/intelligent-artifacts/')
    version = json_obj.get('version', 'latest')

    agent_name = 'gaius-api' + "-" + user_id + "-" + agent_id

    ports = execute_agent(REGISTRY=registry,
                          BIND_PORTS=True,
                          AGENT_ID=agent_id,
                          USER_ID=user_id,
                          KILL=kill,
                          API_KEY=api_key,
                          GENOME=json.dumps(genome),
                          VERSION=version,
                          NETWORK=network)

    if kill:
        return -1
    
    logger.debug(f'started agent with ports {ports}')

    agent_info =  {"name": "",
                   "domain": agent_name,
                   "api_key":api_key,
                   "secure": False}

    return agent_info, ports

def options():
    global options
    parser = OptionParser(version=ia.__version__)
    parser.add_option("-g", "--genome", dest="filename",
                        help="Genome file location", metavar="FILE")

    parser.add_option("--api-key", dest="API_KEY", default='ABCD-1234',
                        help="""Secret API key.
                        Default = 'ABCD-1234'
                                """)

    parser.add_option("--log-level", dest="LOG_LEVEL", default='DEBUG',
                        help="""Log level.
                        Default = DEBUG
                        Options:
                            CRITICAL
                            ERROR
                            WARNING
                            INFO
                            DEBUG
                                """)

    parser.add_option("-n", "--network", dest="NETWORK",
                        help="""Network in which all nodes will communicate.
                        Default = 'g2network'
                                """)
    parser.add_option("--bind-ports", action="store_true", dest="BIND_PORTS", default=False,
                        help="""To enable multiple agents running on single system, port are not bound by default.
                        Specify this option to explicitly bind agent to ports (required to run tests on agent).
                            HTTP port: 8000 + agent_id
                            HTTPS port: 44300 + agent_id
                            """)

    parser.add_option("-b", "--gaius-api-name", dest="BOTTLE", default='gaius-api',
                        help="""Bottle name
                        Default = 'BOTTLE'
                                """)

    parser.add_option("-H", "--hostname", dest="BOTTLE_HOSTNAME", default='localhost',
                        help="""Bottle name
                        Default = 'BOTTLE'
                                """)

    parser.add_option("-r", "--registry", dest="REGISTRY", default='registry.digitalocean.com/intelligent-artifacts/',
                        help="""Container registry
                        Default = 'registry.digitalocean.com/intelligent-artifacts/'

                        Set to '' if you want to use only local containers.
                                """)

    parser.add_option("--container-version", dest="VERSION", default='latest',
                        help="""Version of container images. Same used for all.
                        Default = 'latest'
                        """)

    parser.add_option("-e", "--environment", dest="ENVIRONMENT", default='local',
                        help="""Environment where we're running.
                        Uses config file located at ~/.gaius/setup.ini
                        No need to provide most of the other options when using this.
                        Options taken from the setup.ini file instead.

                        Default = 'local'

                        Ex. 'local' - for local agents using the 'latest' containers
                            'dev'  - to use development containers

                            More to come.
                        """)

    parser.add_option("-d", "--debug",
                        action="store_true", dest="debug", default=False,
                        help="print debug information")

    parser.add_option("--kill",
                        action="store_true", dest="kill", default=False,
                        help="Kill all agent's containers.")

    parser.add_option("--agent-id",
                        dest="agent_id", default="1",
                        help="""A string that uniquely identifies the agent and network. Appended to container and network names
                             Default=1""")
    
    parser.add_option("--user-id",
                        dest="user_id", default=os.environ.get("USER"),
                        help="""A string that uniquely identifies the agent and network. Appended to container and network names
                             Default=os.environ.get("USER")""")
    
    (options, args) = parser.parse_args()

    if not options.filename:
        logger.warn("Need a genome file location! Pass with -g or --genome arg.")
        sys.exit(1)

    if len(options.REGISTRY) > 0 and not options.REGISTRY.endswith('/'):
        options.REGISTRY += '/'

if __name__ == '__main__':
    if not os.path.exists(f"{os.path.expanduser('~')}/.gaius"):
        os.mkdir(f"{os.path.expanduser('~')}/.gaius")
    options()
    
    DEBUG = options.debug
    if DEBUG:
        logger.setLevel(level=logging.DEBUG)
    
    config = configparser.ConfigParser()
    user_dir = os.path.expanduser('~')
    if not os.path.exists(f"{user_dir}/.gaius/setup.ini"):
        print("No setup.ini found! Switching to default values if args not provided. See --help for info.")
        ## Default values provided by OptionParser
        BOTTLE_HOSTNAME = options.BOTTLE_HOSTNAME
        REGISTRY = options.REGISTRY
        VERSION = options.VERSION
        API_KEY = options.API_KEY
        LOG_LEVEL = options.LOG_LEVEL
        NETWORK = options.NETWORK
        BIND_PORTS = options.BIND_PORTS
        

    else:
        if not options.ENVIRONMENT:
            print("environment not provided! Defaulting to 'local'.")
            env = 'local'
        else:
            env = options.ENVIRONMENT
        config.read(f"{user_dir}/.gaius/setup.ini")
        if options.BOTTLE_HOSTNAME:
            BOTTLE_HOSTNAME = options.BOTTLE_HOSTNAME
        else:
            BOTTLE_HOSTNAME = config.get(env, "BOTTLE_HOSTNAME")

        # if options.REGISTRY:
        REGISTRY = options.REGISTRY
        # else:
        #     REGISTRY = config.get(env, "REGISTRY")

        # if options.VERSION:
        VERSION = options.VERSION
        # else:
        #     VERSION = config.get(env, "VERSION")
        BIND_PORTS = options.BIND_PORTS

        if options.API_KEY:
            API_KEY = options.API_KEY
        else:
            API_KEY = config.get(env, "API_KEY")

        if options.LOG_LEVEL:
            LOG_LEVEL = options.LOG_LEVEL
        else:
            LOG_LEVEL = config.get(env, "LOG_LEVEL")

        if options.NETWORK:
            NETWORK = options.NETWORK
        else:
            try:
                NETWORK = config.get(env, "NETWORK")
            except configparser.NoOptionError:
                NETWORK = 'g2network'

    USER_ID = options.user_id
    AGENT_ID = options.agent_id
    configuration = {
                    'BOTTLE_HOSTNAME': BOTTLE_HOSTNAME,
                    'REGISTRY': REGISTRY,
                    'VERSION': VERSION,
                    'API_KEY': API_KEY,
                    'LOG_LEVEL': LOG_LEVEL,
                    'NETWORK': NETWORK,
                    'BIND_PORTS': BIND_PORTS,
                    'user_id' : USER_ID,
                    'agent_id' : AGENT_ID,
                    }

    genome_file = options.filename
    if options.kill:
        stopit(genome_file, user_id=USER_ID, agent_id=AGENT_ID)
        sys.exit(0)

    network = startit(genome_file, **configuration)