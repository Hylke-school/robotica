from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

from get_json import JSON
from sys import argv
json = JSON()


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # TODO: change to specific CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.get_json().encode())
        # print(json.get_json())


def run(server_class=HTTPServer, handler_class=Server, port=5356):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    # httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, keyfile="key.pem", certfile="cert.pem", ssl_version=ssl.PROTOCOL_TLS)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
