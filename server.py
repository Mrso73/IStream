from argparse import ArgumentParser
import socketserver

import http.server
import json


parser = ArgumentParser()
parser.add_argument("-hs", "--host", default="127.0.0.1")
parser.add_argument("-p", "--port", default=8000, type=int)

args = parser.parse_args()



class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'message': 'This is a GET response. Data received successfully.'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # Process the data here
        print("Received POST data:", data)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'message': 'This is a POST response. Data processed successfully.'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))



handler = RequestHandler

with socketserver.TCPServer((str(args.host), args.port), handler) as httpd:
    print("serving at port", args.port)
    httpd.serve_forever()
