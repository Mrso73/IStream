from argparse import ArgumentParser
from http.server import SimpleHTTPRequestHandler
import json
import socketserver


def parse_arguments():
    parser = ArgumentParser(description="Run a simple HTTP server.")
    parser.add_argument("-hs", "--host", default="127.0.0.1", help="Hostname of the server")
    parser.add_argument("-p", "--port", default=8000, type=int, help="Port for the server")
    return parser.parse_args()



class JSONRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/client/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
            print("Received POST data:", data)
            response = {'message': 'Data processed successfully.'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))



def run_server(host, port):
    with socketserver.TCPServer((host, port), JSONRequestHandler) as httpd:
        print(f"Serving at {host}:{port}")
        httpd.serve_forever()



if __name__ == "__main__":
    args = parse_arguments()
    run_server(args.host, args.port)