from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from model import initialize, calculate_data

host = ('localhost', 8897)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers",
                         "Authorization, Content-Type")
        self.end_headers()

        params = self.path[2:].split("&")

        #print(self.path)

        initialize(*map(lambda x: eval(x.split("=")[1]), params))
        #print(json.dumps(calculate_data()))

        self.wfile.write(json.dumps(calculate_data()).encode())


def start_http_service():
    server = HTTPServer(host, RequestHandler)
    print(f"Starting http server, listen at: {host[0]}:{host[1]}")
    server.serve_forever()


start_http_service()
