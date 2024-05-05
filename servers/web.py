from http.server import BaseHTTPRequestHandler
import os
import urllib.parse
import socket
import json

content_file_names = ["index.html", "message.html", "error.html", "style.css", "logo.png", "favicon.ico"]
content_file_names = list(map(lambda x: f"/{x}", content_file_names))


def send_message_data(data: bytes, ip: str = 'localhost', port: int = 5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = ip, port
        sock.connect(server)
        print(f'Connection established {server}')
        print(f'Send data: {data.decode()}')
        sock.send(data)
    print(f'Data transfer completed')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _send_404(self):
        self.send_response(404)
        self.end_headers()
        with open('front/error.html', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the post data
            parsed_data = urllib.parse.parse_qs(post_data.decode())
            data_to_send = {
                'message': parsed_data['message'][0] if 'message' in parsed_data and len(parsed_data['message']) > 0 else None,
                'username': parsed_data['username'][0] if 'username' in parsed_data and len(parsed_data['username']) > 0 else None
            }
            encoded = json.dumps(data_to_send).encode()
            send_message_data(encoded)
            # print(data_to_send)

            self.send_response(302)
            self.send_header('Location', '/message.html')
            self.end_headers()
        else:
            self._send_404()
            return

    def do_GET(self):
        if self.path in content_file_names or self.path == "/":
            if self.path == "/":
                self.path = "/index.html"

            file_path = f'front/{self.path[1:]}'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    if self.path.endswith(".html"):
                        self.send_header('Content-type', 'text/html')
                    elif self.path.endswith(".css"):
                        self.send_header('Content-type', 'text/css')
                    elif self.path.endswith(".png"):
                        self.send_header('Content-type', 'image/png')
                    elif self.path.endswith(".ico"):
                        self.send_header('Content-type', 'image/x-icon')
                    self.end_headers()
                    self.wfile.write(file.read())
            else:
                self._send_404()
        else:
            self._send_404()