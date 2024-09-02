import http.server
import socketserver
import urllib.request
import urllib.error
from itertools import cycle

class LoadBalancer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.server_pools = {
            'servera': cycle(['http://localhost:8881', 'http://localhost:8882']),
            'serverb': cycle(['http://localhost:8883', 'http://localhost:8884'])
        }
        super().__init__(*args, **kwargs)

    def do_GET(self):
        for prefix, pool in self.server_pools.items():
            if self.path.startswith(f'/{prefix}'):
                # Remove the prefix from the path
                modified_path = self.path[len(prefix) + 1:] or '/'
                self.proxy_request(next(pool), modified_path)
                return
        self.send_error(404, "Not Found")

    def proxy_request(self, server_url, path):
        url = f"{server_url}{path}"
        try:
            with urllib.request.urlopen(url) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    if header.lower() != 'transfer-encoding':
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.URLError as e:
            self.send_error(500, f"Server Error: {str(e)}")

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), LoadBalancer) as httpd:
        print(f"Load balancer running on port {PORT}")
        httpd.serve_forever()