"""
DO NOT RENAME THIS MODULE!:
http://www.sidefx.com/docs/houdini/hom/locations.html
Run whenever Houdini is started without a scene file
"""
plugin_info = {
    "name": "Asset Ninja Houdini Asset Import",
    "description": "Handles asset pushes from Asset Ninja.",
    "author": "Aleks Katunar",
    "version": "1.0.0",
}



print("Installing Hook ...")




import sys, imp

sys.modules["assetninja_assetimport"] = imp.new_module("assetninja_assetimport")
sys.modules["assetninja_assetimport"].__name__ = "assetninja_assetimport"
sys.modules["assetninja_assetimport"].__package__ = "\"assetninja_assetimport\""
sys.modules["assetninja_assetimport"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_shared.common.environment"] = imp.new_module("assetninja_assetimport.assetexchange_shared.common.environment")
sys.modules["assetninja_assetimport.assetexchange_shared.common.environment"].__name__ = "assetninja_assetimport.assetexchange_shared.common.environment"
sys.modules["assetninja_assetimport.assetexchange_shared.common.environment"].__package__ = "assetninja_assetimport.assetexchange_shared.common"
sys.modules["assetninja_assetimport.assetexchange_shared.common"] = imp.new_module("assetninja_assetimport.assetexchange_shared.common")
sys.modules["assetninja_assetimport.assetexchange_shared.common"].__name__ = "assetninja_assetimport.assetexchange_shared.common"
sys.modules["assetninja_assetimport.assetexchange_shared.common"].__package__ = "assetninja_assetimport.assetexchange_shared.common"
sys.modules["assetninja_assetimport.assetexchange_shared.common"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_shared.asset.variants"] = imp.new_module("assetninja_assetimport.assetexchange_shared.asset.variants")
sys.modules["assetninja_assetimport.assetexchange_shared.asset.variants"].__name__ = "assetninja_assetimport.assetexchange_shared.asset.variants"
sys.modules["assetninja_assetimport.assetexchange_shared.asset.variants"].__package__ = "assetninja_assetimport.assetexchange_shared.asset"
sys.modules["assetninja_assetimport.assetexchange_shared.asset"] = imp.new_module("assetninja_assetimport.assetexchange_shared.asset")
sys.modules["assetninja_assetimport.assetexchange_shared.asset"].__name__ = "assetninja_assetimport.assetexchange_shared.asset"
sys.modules["assetninja_assetimport.assetexchange_shared.asset"].__package__ = "assetninja_assetimport.assetexchange_shared.asset"
sys.modules["assetninja_assetimport.assetexchange_shared.asset"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_shared.server.services"] = imp.new_module("assetninja_assetimport.assetexchange_shared.server.services")
sys.modules["assetninja_assetimport.assetexchange_shared.server.services"].__name__ = "assetninja_assetimport.assetexchange_shared.server.services"
sys.modules["assetninja_assetimport.assetexchange_shared.server.services"].__package__ = "assetninja_assetimport.assetexchange_shared.server"
sys.modules["assetninja_assetimport.assetexchange_shared.server.registry"] = imp.new_module("assetninja_assetimport.assetexchange_shared.server.registry")
sys.modules["assetninja_assetimport.assetexchange_shared.server.registry"].__name__ = "assetninja_assetimport.assetexchange_shared.server.registry"
sys.modules["assetninja_assetimport.assetexchange_shared.server.registry"].__package__ = "assetninja_assetimport.assetexchange_shared.server"
sys.modules["assetninja_assetimport.assetexchange_shared.server.protocol"] = imp.new_module("assetninja_assetimport.assetexchange_shared.server.protocol")
sys.modules["assetninja_assetimport.assetexchange_shared.server.protocol"].__name__ = "assetninja_assetimport.assetexchange_shared.server.protocol"
sys.modules["assetninja_assetimport.assetexchange_shared.server.protocol"].__package__ = "assetninja_assetimport.assetexchange_shared.server"
sys.modules["assetninja_assetimport.assetexchange_shared.server"] = imp.new_module("assetninja_assetimport.assetexchange_shared.server")
sys.modules["assetninja_assetimport.assetexchange_shared.server"].__name__ = "assetninja_assetimport.assetexchange_shared.server"
sys.modules["assetninja_assetimport.assetexchange_shared.server"].__package__ = "assetninja_assetimport.assetexchange_shared.server"
sys.modules["assetninja_assetimport.assetexchange_shared.server"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_shared.client.registry"] = imp.new_module("assetninja_assetimport.assetexchange_shared.client.registry")
sys.modules["assetninja_assetimport.assetexchange_shared.client.registry"].__name__ = "assetninja_assetimport.assetexchange_shared.client.registry"
sys.modules["assetninja_assetimport.assetexchange_shared.client.registry"].__package__ = "assetninja_assetimport.assetexchange_shared.client"
sys.modules["assetninja_assetimport.assetexchange_shared.client.basic"] = imp.new_module("assetninja_assetimport.assetexchange_shared.client.basic")
sys.modules["assetninja_assetimport.assetexchange_shared.client.basic"].__name__ = "assetninja_assetimport.assetexchange_shared.client.basic"
sys.modules["assetninja_assetimport.assetexchange_shared.client.basic"].__package__ = "assetninja_assetimport.assetexchange_shared.client"
sys.modules["assetninja_assetimport.assetexchange_shared.client"] = imp.new_module("assetninja_assetimport.assetexchange_shared.client")
sys.modules["assetninja_assetimport.assetexchange_shared.client"].__name__ = "assetninja_assetimport.assetexchange_shared.client"
sys.modules["assetninja_assetimport.assetexchange_shared.client"].__package__ = "assetninja_assetimport.assetexchange_shared.client"
sys.modules["assetninja_assetimport.assetexchange_shared.client"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_shared"] = imp.new_module("assetninja_assetimport.assetexchange_shared")
sys.modules["assetninja_assetimport.assetexchange_shared"].__name__ = "assetninja_assetimport.assetexchange_shared"
sys.modules["assetninja_assetimport.assetexchange_shared"].__package__ = "assetninja_assetimport.assetexchange_shared"
sys.modules["assetninja_assetimport.assetexchange_shared"].__path__ = []
sys.modules["assetninja_assetimport.assetexchange_houdini.plugin"] = imp.new_module("assetninja_assetimport.assetexchange_houdini.plugin")
sys.modules["assetninja_assetimport.assetexchange_houdini.plugin"].__name__ = "assetninja_assetimport.assetexchange_houdini.plugin"
sys.modules["assetninja_assetimport.assetexchange_houdini.plugin"].__package__ = "assetninja_assetimport.assetexchange_houdini"
sys.modules["assetninja_assetimport.assetexchange_houdini"] = imp.new_module("assetninja_assetimport.assetexchange_houdini")
sys.modules["assetninja_assetimport.assetexchange_houdini"].__name__ = "assetninja_assetimport.assetexchange_houdini"
sys.modules["assetninja_assetimport.assetexchange_houdini"].__package__ = "assetninja_assetimport.assetexchange_houdini"
sys.modules["assetninja_assetimport.assetexchange_houdini"].__path__ = []
sys.modules["assetninja_assetimport.assetimport_houdini.importer.surface_maps"] = imp.new_module("assetninja_assetimport.assetimport_houdini.importer.surface_maps")
sys.modules["assetninja_assetimport.assetimport_houdini.importer.surface_maps"].__name__ = "assetninja_assetimport.assetimport_houdini.importer.surface_maps"
sys.modules["assetninja_assetimport.assetimport_houdini.importer.surface_maps"].__package__ = "assetninja_assetimport.assetimport_houdini.importer"
sys.modules["assetninja_assetimport.assetimport_houdini.importer.environment_hdri"] = imp.new_module("assetninja_assetimport.assetimport_houdini.importer.environment_hdri")
sys.modules["assetninja_assetimport.assetimport_houdini.importer.environment_hdri"].__name__ = "assetninja_assetimport.assetimport_houdini.importer.environment_hdri"
sys.modules["assetninja_assetimport.assetimport_houdini.importer.environment_hdri"].__package__ = "assetninja_assetimport.assetimport_houdini.importer"
sys.modules["assetninja_assetimport.assetimport_houdini.importer"] = imp.new_module("assetninja_assetimport.assetimport_houdini.importer")
sys.modules["assetninja_assetimport.assetimport_houdini.importer"].__name__ = "assetninja_assetimport.assetimport_houdini.importer"
sys.modules["assetninja_assetimport.assetimport_houdini.importer"].__package__ = "assetninja_assetimport.assetimport_houdini.importer"
sys.modules["assetninja_assetimport.assetimport_houdini.importer"].__path__ = []
sys.modules["assetninja_assetimport.assetimport_houdini.pushservice"] = imp.new_module("assetninja_assetimport.assetimport_houdini.pushservice")
sys.modules["assetninja_assetimport.assetimport_houdini.pushservice"].__name__ = "assetninja_assetimport.assetimport_houdini.pushservice"
sys.modules["assetninja_assetimport.assetimport_houdini.pushservice"].__package__ = "assetninja_assetimport.assetimport_houdini"
sys.modules["assetninja_assetimport.assetimport_houdini"] = imp.new_module("assetninja_assetimport.assetimport_houdini")
sys.modules["assetninja_assetimport.assetimport_houdini"].__name__ = "assetninja_assetimport.assetimport_houdini"
sys.modules["assetninja_assetimport.assetimport_houdini"].__package__ = "assetninja_assetimport.assetimport_houdini"
sys.modules["assetninja_assetimport.assetimport_houdini"].__path__ = []


setattr(sys.modules["assetninja_assetimport.assetexchange_shared.common"], "environment", sys.modules["assetninja_assetimport.assetexchange_shared.common.environment"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared"], "common", sys.modules["assetninja_assetimport.assetexchange_shared.common"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.asset"], "variants", sys.modules["assetninja_assetimport.assetexchange_shared.asset.variants"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared"], "asset", sys.modules["assetninja_assetimport.assetexchange_shared.asset"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.server"], "services", sys.modules["assetninja_assetimport.assetexchange_shared.server.services"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.server"], "registry", sys.modules["assetninja_assetimport.assetexchange_shared.server.registry"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.server"], "protocol", sys.modules["assetninja_assetimport.assetexchange_shared.server.protocol"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared"], "server", sys.modules["assetninja_assetimport.assetexchange_shared.server"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.client"], "registry", sys.modules["assetninja_assetimport.assetexchange_shared.client.registry"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared.client"], "basic", sys.modules["assetninja_assetimport.assetexchange_shared.client.basic"])
setattr(sys.modules["assetninja_assetimport.assetexchange_shared"], "client", sys.modules["assetninja_assetimport.assetexchange_shared.client"])
setattr(sys.modules["assetninja_assetimport"], "assetexchange_shared", sys.modules["assetninja_assetimport.assetexchange_shared"])
setattr(sys.modules["assetninja_assetimport.assetexchange_houdini"], "plugin", sys.modules["assetninja_assetimport.assetexchange_houdini.plugin"])
setattr(sys.modules["assetninja_assetimport"], "assetexchange_houdini", sys.modules["assetninja_assetimport.assetexchange_houdini"])
setattr(sys.modules["assetninja_assetimport.assetimport_houdini.importer"], "surface_maps", sys.modules["assetninja_assetimport.assetimport_houdini.importer.surface_maps"])
setattr(sys.modules["assetninja_assetimport.assetimport_houdini.importer"], "environment_hdri", sys.modules["assetninja_assetimport.assetimport_houdini.importer.environment_hdri"])
setattr(sys.modules["assetninja_assetimport.assetimport_houdini"], "importer", sys.modules["assetninja_assetimport.assetimport_houdini.importer"])
setattr(sys.modules["assetninja_assetimport.assetimport_houdini"], "pushservice", sys.modules["assetninja_assetimport.assetimport_houdini.pushservice"])
setattr(sys.modules["assetninja_assetimport"], "assetimport_houdini", sys.modules["assetninja_assetimport.assetimport_houdini"])



print("Hooks done.")




exec '''import os
import errno


def lookup_assetexchange_path(*parts):
    path = os.path.expanduser("~")
    # workaround required for 2.7, because HOME is checked on windows and sometimes set to Document folder (which is wrong)
    if os.name == \'nt\':
        if \'USERPROFILE\' in os.environ:
            path = os.environ[\'USERPROFILE\']
        else:
            try:
                drive = os.environ[\'HOMEDRIVE\']
            except KeyError:
                drive = \'\'
            path = os.path.join(drive, os.environ[\'HOMEPATH\'])
    path = os.path.join(path, ".assetexchange", *parts)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def services_path(*parts):
    return lookup_assetexchange_path(\'services\', *parts)
''' in sys.modules["assetninja_assetimport.assetexchange_shared.common.environment"].__dict__

exec '''from .environment import *
''' in sys.modules["assetninja_assetimport.assetexchange_shared.common"].__dict__

exec '''import itertools


def explode_variants(assemblyName, variants):
    if assemblyName not in variants:
        return ([], [])
    # build cartesian product out of provided variants
    labels = list(variants[assemblyName].keys())
    configs = itertools.product(*list(variants[assemblyName].values()))
    return (labels, configs)


def filter_objects_by_variant_config(asset, assemblyName, variantLabels, variantConfig):
    if assemblyName not in asset[\'assemblies\']:
        return []

    def filter_by_config(obj):
        for obj_variant in obj[\'variants\']:
            matches = True
            for idx, label in enumerate(variantLabels):
                if variantConfig[idx] != obj_variant[label]:
                    matches = False
            if matches:
                return True
        return False
    return list(filter(filter_by_config, list(asset[\'assemblies\'][assemblyName][\'objects\'].values())))
''' in sys.modules["assetninja_assetimport.assetexchange_shared.asset.variants"].__dict__

exec '''from .variants import *
''' in sys.modules["assetninja_assetimport.assetexchange_shared.asset"].__dict__

exec '''
class AssetPushServiceInterface:
    # lists all supported asset types which can be pushed here
    def SupportedTypes(self, _):
        return []

    # checks if specific asset can be pushed here
    def PushAllowed(self, asset):
        return False

    # reacts to asset push intent
    def Push(self, data):
        return False
''' in sys.modules["assetninja_assetimport.assetexchange_shared.server.services"].__dict__

exec '''import os
from .. import common


def service_entry_path(category, type):
    return os.path.join(common.services_path(category, type), str(os.getpid()))
''' in sys.modules["assetninja_assetimport.assetexchange_shared.server.registry"].__dict__

exec '''import json
import logging

try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    from http.server import BaseHTTPRequestHandler
try:
  basestring
except NameError:
  basestring = str

class HttpServerRequestHandler(BaseHTTPRequestHandler):
    # retrieves logger (will be overriden)
    def get_logger(self):
        return logging.getLogger()

    # retrieves service registry (will be overriden)
    def get_service_registry(self):
        return {}

    # apply our logging mechanism
    def log_message(self, format, *args):
        #logger = self.get_logger()
        #logger.info(format % args)
        pass

    # handle post request
    def do_POST(self):
        logger = self.get_logger()
        try:
            # load and parse request
            req_raw = self.rfile.read(int(self.headers.get(\'content-length\')))
            req_msg = {
                "id": 0,
                "address": None,
                "input": None,
                "final": True
            }
            req_msg.update(json.loads(req_raw))
            try:
                # validate request
                if \'address\' not in req_msg or not isinstance(req_msg[\'address\'], basestring):
                    raise RuntimeError(\'address_missing\')
                if \'final\' not in req_msg or req_msg[\'final\'] != True:
                    raise RuntimeError(\'request_not_final\')
                # extract service and function name
                address_parts = req_msg[\'address\'].split(".")
                service_name = ".".join(address_parts[:-1])
                function_name = address_parts[-1]
                # lookup service
                service_registry = self.get_service_registry()
                if service_name not in service_registry or service_registry[service_name] is None:
                    raise RuntimeError(\'unknown_service\')
                service_class = service_registry[service_name]
                service = service_class()
                # lookup function
                function = getattr(service, function_name, None)
                if not callable(function):
                    raise RuntimeError(\'unknown_function\')
                # call function (will be delegated to main thread automatically, when annotated)
                #logger.info(\'executing \' + req_msg[\'address\'])
                res_msg = {
                    "id": req_msg["id"],
                    "output": function(req_msg["input"]),
                    "error": None,
                    "last": True
                }
                # write response
                self.send_response(200)
                self.send_header(\'Content-type\', \'application/json\')
                self.end_headers()
                self.wfile.write(json.dumps(res_msg).encode())
            except Exception as e:
                logger.exception("exception occured in post handler")
                # prepare response
                res_msg = {
                    "id": req_msg["id"],
                    "output": None,
                    "error": str(e),
                    "last": True
                }
                # write response
                self.send_response(200)
                self.send_header(\'Content-type\', \'application/json\')
                self.end_headers()
                self.wfile.write(json.dumps(res_msg).encode())
        except Exception as e:
            logger.exception("exception occured in post handler")
            # write response
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def end_headers(self):
        self.send_header(\'Access-Control-Allow-Origin\', \'*\')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header(\'Access-Control-Allow-Methods\', \'GET, POST, OPTIONS\')
        BaseHTTPRequestHandler.end_headers(self)
''' in sys.modules["assetninja_assetimport.assetexchange_shared.server.protocol"].__dict__

exec '''from .protocol import *
from .registry import *
from .services import *
''' in sys.modules["assetninja_assetimport.assetexchange_shared.server"].__dict__

exec '''import os
import json
from .. import common

def lookup_port(category, type):
    regDir = common.services_path(category, type)
    pidfiles = [fn for fn in os.listdir(regDir) if (
        os.path.isfile(os.path.join(regDir, fn)) and fn.isdigit())]
    if len(pidfiles) > 0:
        with open(os.path.join(regDir, pidfiles[0]), \'r\') as file:
            node = json.loads(file.read())
            return node[\'port\']
    else:
        raise RuntimeError(\'could not lookup port for \' +
                           category + \'/\' + type)
''' in sys.modules["assetninja_assetimport.assetexchange_shared.client.registry"].__dict__

exec '''import json

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def call_basic_func(port, service, function, input, timeout):

    # prepare url
    url = "http://127.0.0.1:" + str(port) + "/.assetexchange/basic"

    # prepare timeout
    if timeout == 0:
        timeout = 10

    # prepare request message
    reqMsg = {
        \'id\': 0,
        \'address\': service + \'.\' + function,
        \'input\': input,
        \'final\': True
    }
    reqMsgByte = json.dumps(reqMsg).encode(\'utf8\')

    # execute request
    req = Request(
        url, data=reqMsgByte, method="POST",
        headers={\'content-type\': \'application/json\'}
    )

    # read response message
    res = urlopen(req, timeout=timeout)
    resMsg = json.loads(res.read().decode(\'utf-8\'))

    # raise error if one occured
    if resMsg[\'error\'] is not None:
        raise RuntimeError(resMsg[\'error\'])

    return resMsg[\'output\']
''' in sys.modules["assetninja_assetimport.assetexchange_shared.client.basic"].__dict__

exec '''from .basic import *
from .registry import *
''' in sys.modules["assetninja_assetimport.assetexchange_shared.client"].__dict__

exec '''from . import common
from . import asset
from . import client
from . import server
''' in sys.modules["assetninja_assetimport.assetexchange_shared"].__dict__

print "Modules created."



try:
    import assetninja_assetimport.assetexchange_houdini as assetexchange_houdini
    import assetninja_assetimport.assetimport_houdini as assetimport_houdini
    print "imports ok"

    def initializePlugin():
        assetexchange_houdini.register_plugin("assetninja.extension.houdini.assetimport", plugin_info, assetimport_houdini.AssetPushService)

    def uninitializePlugin():
        assetexchange_houdini.unregister_plugin("assetninja.extension.houdini.assetimport")
except:
    print "imports not ok"
