from http.server import BaseHTTPRequestHandler
import socketserver
import yaml
from utilities.config_loader import get_config

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, handlers, *args, **kwargs):
        self.handlers = handlers
        super().__init__(*args, **kwargs)

    def do_GET(self):
        request_path = self.path.split("/")[-1]
        if request_path in self.handlers:
            response = self.handlers[request_path]()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>COVID Analysis API</title>
            </head>
            <body>
                <h1>COVID-19 Analysis API Endpoints</h1>
                <hr>
                <p>Available analysis options:</p>
                <ul>
            """
            for key in self.handlers.keys():
                html_content += f'<li><a href="/{key}">{key.replace("_", " ")}</a></li>'
            html_content += """
                </ul>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())

class MyTCPServer(socketserver.TCPServer):
    def server_close(self):
        super().server_close()
        print("Socket released.")

def run_server(handlers):
    config = get_config()
    host = config['server']['host']
    port = config['server']['port']
    
    with MyTCPServer((host, port), lambda *args, **kwargs: RequestHandler(handlers, *args, **kwargs)) as httpd:
        print(f"Serving at http://{host}:{port}")
        httpd.serve_forever()
