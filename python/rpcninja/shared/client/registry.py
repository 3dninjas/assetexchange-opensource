import os
import json
from .. import environment


def rpc_lookup_port(category, type):
    regDir = environment.registry_root_dir(category, type)
    pidfiles = [fn for fn in os.listdir(regDir) if (
        os.path.isfile(os.path.join(regDir, fn)) and fn.isdigit())]
    if len(pidfiles) > 0:
        with open(os.path.join(regDir, pidfiles[0]), 'r') as file:
            node = json.loads(file.read())
            return node['port']
    else:
        raise RuntimeError('could not lookup port for ' +
                           category + '/' + type)
