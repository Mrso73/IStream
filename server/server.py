from argparse import ArgumentParser
from http.server import SimpleHTTPRequestHandler, HTTPServer

import socketserver
import webbrowser
import json
import os



class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = os.path.join(os.path.dirname(__file__), '../client')
        super().__init__(*args, directory=self.directory, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

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



def parse_arguments():
    parser = ArgumentParser(description="Run a simple HTTP server.")
    parser.add_argument("-hs", "--host", default="127.0.0.1", help="Hostname of the server")
    parser.add_argument("-pr", "--port", default=8000, type=int, help="Port for the server")
    parser.add_argument("-l", "--launch", default=False, help="Launch server in web browser")
    return parser.parse_args()



def run_server(host, port, open_browser):
    handler_class = CustomHTTPRequestHandler
    server_address = (host, port)
    httpd = HTTPServer(server_address, handler_class)

    url = f"http://{host}:{port}"
    print(f"Serving at {url}")

    if open_browser:
        webbrowser.open(url)

    httpd.serve_forever()



if __name__ == "__main__":
    args = parse_arguments()
    run_server(args.host, args.port, args.launch)