from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.path = '/../web_src/index.html'
        elif self.path == '/app.js':
            self.path = '/../web_src/app.js'

        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
        print(file_to_open)


def run_http_server():
    httpd = HTTPServer(('', 8080), Serv)
    httpd.serve_forever()


if __name__ == "__main__":
    run_http_server()