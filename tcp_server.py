from socketserver import ThreadingTCPServer, StreamRequestHandler
from threading import Thread, Event
from signal import signal, SIGINT
from select import select
from argparse import ArgumentParser


class RequestHandler(StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.timeout = 10
        super().__init__(request, client_address, server)

    def handle(self):
        while True:
            # Use select() with small timeout to increase 
            # the responsiveness to shutdown requests.
            rdy_to_read, _, _ = select([self.rfile], [], [], 1)
            
            if self.server.shutdown_flag:
                break

            if self.rfile in rdy_to_read:
                try:
                    data = self.rfile.readline()
                    if not data:
                        break
                    self.wfile.write(data)
                except (TimeoutError, ConnectionAbortedError):
                    break


class Server(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.shutdown_flag = False

    def shutdown(self):
        self.shutdown_flag = True
        super().shutdown()
        

def termination_handler(server, term_event):
    term_event.wait()
    server.shutdown()


def main(host, port):
    server = Server((host, port), RequestHandler)

    # As specified in the socketserver docs, we need a 
    # separate thread to shutdown the server.
    term_event = Event()
    term_listener = Thread(target=termination_handler, args=(server, term_event))
    term_listener.start()

    def sigint_handler(*_):
        term_event.set()

    signal(SIGINT, sigint_handler)

    server.serve_forever() # Handle one request at a time until shutdown.
    term_listener.join()


if __name__ == '__main__':
    ap = ArgumentParser(description='Simple tcp server')
    ap.add_argument('host', type=str, help='The hostname or IP address to bind the server to')
    ap.add_argument('port', type=int, help='The port number on which the server will listen')
    args = ap.parse_args()
    main(args.host, args.port)
