from argparse import ArgumentParser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser
import json
import os

import inference as llm



class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler to serve files and handle POST requests."""

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.path.join(os.path.dirname(__file__), '../client')
        super().__init__(*args, directory=directory, **kwargs)


    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()


    def do_POST(self):
        """Handle POST from frontend"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            print("Received POST data")

            b64_string = data.get("image", "")[22:]
            comment_list = llm.generate_comments(b64_string) 

            response = {
                'comments': comment_list
            }
            self._send_response(200, response)
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))


    def _send_response(self, status_code, data):
        """Send HTTP response with given status code and data."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

        

def parse_arguments():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Run a simple HTTP server.")
    parser.add_argument("-hs", "--host", default="127.0.0.1", help="Hostname of the server") 
    parser.add_argument("-pr", "--port", default=8000, type=int, help="Port for the server")
    parser.add_argument("-l", "--launch", default=False, type=bool, help="Launch server in web browser")
    return parser.parse_args()



def run_server(host, port, open_browser):
    """Run the HTTP server."""
    handler_class = CustomHTTPRequestHandler
    server_address = (host, port)
    httpd = HTTPServer(server_address, handler_class)

    url = f"http://{host}:{port}"
    print(f"Serving at {url}")

    if open_browser:
        webbrowser.open_new_tab(url)

    httpd.serve_forever()



if __name__ == "__main__":
    args = parse_arguments()
    run_server(args.host, args.port, args.launch)