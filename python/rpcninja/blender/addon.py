import os
import time
import threading
import http
import json
import sys
import atexit
import logging
import bpy
from .. import shared
from . import mainthread


_loggers = dict()
_http_servers = dict()


def _prepare_logger(addon_uid):
    global _loggers

    # return existing logger
    if addon_uid in _loggers:
        return _loggers[addon_uid]

    # create logger
    logger = logging.getLogger(addon_uid)
    logger.setLevel(logging.INFO)

    # add console handler
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    console_log.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_log)

    # register logger
    _loggers[addon_uid] = logger
    return logger


def register_addon(addon_uid, bl_info, AssetPushService=None, misc_services={}):
    # prevent double registration
    global _http_servers
    if addon_uid in _http_servers:
        raise RuntimeError('add-on already registered')

    # create logger
    logger = _prepare_logger(addon_uid)

    # check if push service is derived properly
    if AssetPushService is not None:
        if not issubclass(AssetPushService, shared.server.AssetPushServiceInterface):
            raise RuntimeError(
                'AssetPushService should inherit AssetPushServiceInterface')

    # setup registry
    service_registry = {}
    if AssetPushService is not None:
        service_registry['assetninja.assetpush#1'] = AssetPushService
    service_registry.update(misc_services)
    service_registry = {key: val for key,
                        val in service_registry.items() if val is not None}

    # setup http protocol handler
    class HttpServerRequestHandler(shared.server.HttpServerRequestHandler):
        # copy logger over
        _logger = logger

        # override logger getter
        def get_logger(self):
            return self._logger

        # copy service registry over
        _service_registry = service_registry

        # override service registry getter
        def get_service_registry(self):
            return self._service_registry

    # start http server using a free port
    _http_servers[addon_uid] = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0),
        HttpServerRequestHandler
    )
    thread = threading.Thread(
        target=_http_servers[addon_uid].serve_forever)
    # note: required for blender exit, otherwhise it will block (even though we have an atexit handler)
    thread.setDaemon(True)
    thread.start()

    # retrieve port (no race condition here, as it is available right after construction)
    port = _http_servers[addon_uid].server_address[1]
    logger.info("port=" + str(port))

    # write registration file
    regfile = shared.server.registration_path(
        'extension.blender', addon_uid)
    with open(regfile, 'w') as portfile:
        portfile.write(json.dumps({
            'environment': shared.common.environment_name(),
            'category': 'extension.blender',
            'type': addon_uid,
            'pid': os.getpid(),
            'port': port,
            'protocols': ['basic'],
            'info': {
                'extension.uid': addon_uid,
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
def unregister_addon(addon_uid):
    # prepare logger
    logger = _prepare_logger(addon_uid)

    # remove main thread task handler
    if bpy.app.timers.is_registered(mainthread.main_thread_handler):
        logger.info('removing main thread task handler')
        bpy.app.timers.unregister(mainthread.main_thread_handler)

    # try to remove registration file
    regfile = shared.server.registration_path(
        'extension.blender', addon_uid)
    for _ in range(5):
        if os.path.exists(regfile):
            try:
                logger.info('trying to remove registration file')
                os.remove(regfile)
            except Exception:
                logger.exception(
                    "assetninja: could not remove registration file")
                time.sleep(1)
                continue
            else:
                break
        else:
            break

    # shutdown server
    global _http_servers
    if addon_uid in _http_servers:
        logger.info('shutdown http server')
        _http_servers[addon_uid].shutdown()
        del _http_servers[addon_uid]

    # execute all pending tasks (in my mind this might prevent deadlocks, maybe?)
    mainthread.main_thread_handler()
