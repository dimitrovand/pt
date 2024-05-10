from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
PORT = 50001


if __name__ == "__main__":
    while True:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((HOST, PORT))  

            with s.makefile('r') as rfile:
                while True:
                    m = input('tx msg: ')
                    s.sendall((m + '\n').encode()) 
                    m = rfile.readline().strip()
                    print("rx msg:", m)