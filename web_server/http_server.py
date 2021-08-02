from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        print('want path:', self.path)
        is_image = False
        if self.path == '/':
            self.path = '../web_src/index.html'
        elif self.path == '/app.js':
            self.path = '../web_src/app.js'
        elif self.path == '/jquery.min.js':
            self.path = '../web_src/jquery.min.js'
        elif self.path == '/style.css':
            self.path = '../web_src/style.css'
        elif self.path == '/arrow.png':
            self.path = '../web_src/arrow.png'
            is_image = True
        elif self.path == '/arrow-left.svg':
            self.path = '../web_src/arrow-left.svg'
        elif self.path == '/helicopter.png':
            self.path = '../web_src/helicopter.png'
            is_image = True

        try:
            if is_image:
                file_to_open = open(self.path, 'rb').read()
            else:
                file_to_open = open(self.path).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        if is_image:
            self.wfile.write(file_to_open)
        else:
            self.wfile.write(bytes(file_to_open, 'utf-8'))


def run_http_server():
    httpd = HTTPServer(('', 8080), Serv)
    httpd.serve_forever()


if __name__ == "__main__":
    run_http_server()