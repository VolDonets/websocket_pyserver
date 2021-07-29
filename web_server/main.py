import websocket_server
import http_server
import my_thread

if __name__ == "__main__":
    http_server_thread = my_thread.MyThread("HTTP server", http_server.run_http_server)

    http_server_thread.start()
    websocket_server.run_web_socket_server()
