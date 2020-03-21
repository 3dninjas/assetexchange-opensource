import os
import time
import json
import sys
import atexit
import logging
import BaseHTTPServer
import SocketServer
import assetexchange_shared
import ix


_http_servers = dict()


class ServerLoop:
    def cycle(self):
        global _http_servers
        # needs a bit of improvement here, but fine for first iteration
        for plugin_uid in list(_http_servers.keys()):
            _http_servers[plugin_uid].handle_request()
        # calling check_for_events is required to keep CPU low
        ix.application.check_for_events()
        # schedule next iteration
        ix.application.add_to_event_loop_single(self.cycle)


ServerLoop().cycle()


def register_plugin(plugin_uid, plugin_info, AssetPushService=None, misc_services={}):
    # prevent double registration
    global _http_servers
    if plugin_uid in _http_servers:
        raise RuntimeError('add-on already registered')

    # prepare logger
    logger = logging.getLogger(plugin_uid)
    logger.setLevel(logging.INFO)

    # add console handler
    if not hasattr(logger, '_has_console_handler'):
        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG)
        console_log.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_log)
        setattr(logger, '_has_console_handler', True)

    # check if push service is derived properly
    if AssetPushService is not None:
        if not issubclass(AssetPushService, assetexchange_shared.server.AssetPushServiceInterface):
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
    class HttpServerRequestHandler(assetexchange_shared.server.HttpServerRequestHandler):
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
    _http_servers[plugin_uid] = BaseHTTPServer.HTTPServer(
        ('127.0.0.1', 0),
        HttpServerRequestHandler
    )
    _http_servers[plugin_uid].timeout = 0

    # retrieve port (no race condition here, as it is available right after construction)
    port = _http_servers[plugin_uid].server_address[1]
    #logger.info("port=" + str(port))

    # write registration file
    regfile = assetexchange_shared.server.service_entry_path(
        'extension.clarisse', plugin_uid)
    with open(regfile, 'w') as portfile:
        portfile.write(json.dumps({
            'category': 'extension.clarisse',
            'type': plugin_uid,
            'pid': os.getpid(),
            'port': port,
            'protocols': ['basic'],
            'info': {
                'extension.uid': plugin_uid,
                'extension.name': plugin_info['name'],
                'extension.description': plugin_info['description'],
                'extension.author': plugin_info['author'],
                'extension.version': plugin_info['version'],
                'clarisse.executable': sys.executable,
                'clarisse.version': 'TODO',  # TODO
            },
            'services': list(service_registry.keys()),
        }, indent=2))


def unregister_plugin(plugin_uid):
    # fetch logger
    logger = logging.getLogger(plugin_uid)

    # try to remove registration file
    regfile = assetexchange_shared.server.service_entry_path(
        'extension.clarisse', plugin_uid)
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
    if plugin_uid in _http_servers:
        logger.info('shutdown http server')
        _http_servers[plugin_uid].shutdown()
        del _http_servers[plugin_uid]


@atexit.register
def unregister_plugins():
    global _http_servers
    for plugin_uid in list(_http_servers.keys()):
        unregister_plugin(plugin_uid)
