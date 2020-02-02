import os
import time
import threading
import http
import json
import sys
import atexit
import bpy
from .. import shared
from . import mainthread

_extension_uid = None
_http_server = None


def register_addon(extension_uid, bl_info, AssetPushService=None, misc_services={}):
    global _extension_uid
    global _http_server
    #global _logger

    # copy extension id
    _extension_uid = extension_uid

    # create logger
    # if _logger is logging.getLogger():
    #     _logger = logging.getLogger(extension_uid)
    #     _logger.setLevel(logging.INFO)

    #     console_log = logging.StreamHandler()
    #     console_log.setLevel(logging.DEBUG)
    #     console_log.setFormatter(logging.Formatter(
    #         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    #     _logger.addHandler(console_log)

    # check if extension service is derived properly
    if AssetPushService is not None:
        if not issubclass(AssetPushService, shared.server.AssetPushServiceInterface):
            raise RuntimeError(
                'AssetPushService should inherit AssetPushServiceInterface')

    # prevent double registration
    if _http_server is not None:
        raise RuntimeError('extension already registered')

    # setup registry
    service_registry = {}
    if AssetPushService is not None:
        service_registry['assetninja.assetpush#1'] = AssetPushService
    service_registry.update(misc_services)
    service_registry = {key: val for key,
                        val in service_registry.items() if val is not None}

    class LocalHttpServerRequestHandler(shared.server.HttpServerRequestHandler):
        # copy service registry over
        _service_registry = service_registry

        # override service_registry getter
        def get_service_registry(self):
            return self._service_registry

    # start http server using a free port
    _http_server = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0),
        LocalHttpServerRequestHandler
    )
    thread = threading.Thread(target=_http_server.serve_forever)
    # note: required for blender exit, otherwhise it will block (even though we have an atexit handler)
    thread.setDaemon(True)
    thread.start()

    # retrieve port (no race condition here, as it is available right after construction)
    port = _http_server.server_address[1]
    #_logger.info("port=" + str(port))

    # write registration file
    regfile = shared.server.registration_path(
        'extension.blender', _extension_uid)
    with open(regfile, 'w') as portfile:
        portfile.write(json.dumps({
            'environment': shared.common.environment_name(),
            'category': 'extension.blender',
            'type': extension_uid,
            'pid': os.getpid(),
            'port': port,
            'protocols': ['basic'],
            'info': {
                'extension.uid': _extension_uid,
                'extension.name': bl_info.get('name', None),
                'extension.description': bl_info.get('description', None),
                'extension.author': bl_info.get('author', None),
                'extension.version': '.'.join(map(str, bl_info.get('version'))) if 'version' in bl_info else None,
                'blender.executable': sys.executable,
                'blender.version': '.'.join(map(str, bpy.app.version)),
                'blender.user_scripts': bpy.utils.user_resource('SCRIPTS'),
            },
            'services': list(service_registry.keys()),
        }, indent=2))

    # register main thread task handler
    bpy.app.timers.register(mainthread.main_thread_handler,
                            first_interval=1.0, persistent=True)


@atexit.register
def unregister_addon():
    global _http_server
    #global _logger

    # remove main thread task handler
    if bpy.app.timers.is_registered(mainthread.main_thread_handler):
        #_logger.info('removing main thread task handler')
        bpy.app.timers.unregister(mainthread.main_thread_handler)

    # try to remove registration file
    regfile = shared.server.registration_path(
        'extension.blender', _extension_uid)
    for _ in range(5):
        if os.path.exists(regfile):
            try:
                #_logger.info('trying to remove registration file')
                os.remove(regfile)
            except Exception:
                # _logger.exception(
                #     "assetninja: could not remove registration file")
                time.sleep(1)
                continue
            else:
                break
        else:
            break

    # shutdown server
    if _http_server is not None:
        #_logger.info('shutdown http server')
        _http_server.shutdown()
        _http_server = None

    # execute all pending tasks (in my mind this might prevent deadlocks, maybe?)
    mainthread.main_thread_handler()
