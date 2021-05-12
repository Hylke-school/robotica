from http.server import BaseHTTPRequestHandler, HTTPServer

from get_json import JSON
from sys import argv


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(JSON().get_json())


def run(server_class=HTTPServer, handler_class=Server, port=5356):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
