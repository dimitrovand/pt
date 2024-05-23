from socket import socket, AF_INET, SOCK_STREAM
from argparse import ArgumentParser


def main(host, port):
    while True:
        try:
            with socket(AF_INET, SOCK_STREAM) as s, s.makefile('r') as rf, s.makefile('w') as wf:
                s.settimeout(2)
                s.connect((host, port))

                while True:
                    m = input('tx msg: ')
                    wf.write(m + '\n')  # Ensure the message is newline terminated
                    wf.flush()  # Flush the buffer to send the data immediately
                    m = rf.readline().strip()
                    print("rx msg:", m)
        except (KeyboardInterrupt, TypeError):
            break
        except Exception as e:
            print(f'{e}')


if __name__ == '__main__':
    ap = ArgumentParser(description='Simple tcp client')
    ap.add_argument('host', type=str, help='The hostname or IP address of the server to connect to')
    ap.add_argument('port', type=int, help='The port number on which the server is listening')
    args = ap.parse_args()
    main(args.host, args.port)

