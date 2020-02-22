import json
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
            req_raw = self.rfile.read(int(self.headers.get('content-length')))
            req_msg = {
                "id": 0,
                "address": None,
                "input": None,
                "final": True
            }
            req_msg.update(json.loads(req_raw))
            try:
                # validate request
                if 'address' not in req_msg or not isinstance(req_msg['address'], basestring):
                    raise RuntimeError('address_missing')
                if 'final' not in req_msg or req_msg['final'] != True:
                    raise RuntimeError('request_not_final')
                # extract service and function name
                address_parts = req_msg['address'].split(".")
                service_name = ".".join(address_parts[:-1])
                function_name = address_parts[-1]
                # lookup service
                service_registry = self.get_service_registry()
                if service_name not in service_registry or service_registry[service_name] is None:
                    raise RuntimeError('unknown_service')
                service_class = service_registry[service_name]
                service = service_class()
                # lookup function
                function = getattr(service, function_name, None)
                if not callable(function):
                    raise RuntimeError('unknown_function')
                # call function (will be delegated to main thread automatically, when annotated)
                logger.info('executing ' + req_msg['address'])
                res_msg = {
                    "id": req_msg["id"],
                    "output": function(req_msg["input"]),
                    "error": None,
                    "last": True
                }
                # write response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
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
                self.send_header('Content-type', 'application/json')
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
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        BaseHTTPRequestHandler.end_headers(self)
