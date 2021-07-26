import websocket_server
import http_server

from threading import Thread

class MyThread(Thread):
    def __init__(self, name, func_to_run):
        Thread.__init__(self)
        self.name = name
        self.func_to_run = func_to_run

    def run(self):
        print(str(self.name) + " thread is running")
        self.func_to_run()


if __name__ == "__main__":
    http_server_thread = MyThread("HTTP server", http_server.run_http_server)

    http_server_thread.start()
    websocket_server.run_web_socket_server()
