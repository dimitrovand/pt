from socketserver import ThreadingTCPServer, StreamRequestHandler
from threading import Thread
from signal import signal, SIGINT

HOST = 'localhost'
PORT = 50001


class RequestHandler(StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.timeout = 10
        super().__init__(request, client_address, server)

    def handle(self):
        while True:
            try:
                command = self.rfile.readline()
            except TimeoutError:
                break

            if not command:
                break

            self.wfile.write(command)


class Server(ThreadingTCPServer):
    pass


if __name__ == "__main__":
    server = Server((HOST, PORT), RequestHandler)

    def termination_handler():
        server.shutdown()

    termination = Thread(target=termination_handler)

    def sigint_handler(signal, frame):
        termination.start()

    signal(SIGINT, sigint_handler)
    server.serve_forever()
    termination.join()
