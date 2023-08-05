from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

from . import pythoninfo


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(pythoninfo().encode())


def run(host='localhost', port=8000):
    server_address = (host, int(port))
    httpd = HTTPServer(server_address, HttpGetHandler)
    try:
        print('Open URL to show info: http://%s:%d' % server_address)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    return 0


if __name__ == '__main__':
    address = sys.argv[1:]

    if len(address) > 2:
        sys.exit(1)

    sys.exit(run(*address))
