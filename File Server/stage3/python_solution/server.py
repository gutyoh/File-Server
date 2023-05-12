# create a constant PORT
import socket

PORT = 12345

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", PORT)
    sock.bind(server_address)

    sock.listen(1)
    print("Server started!")
    while True:
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    print("Received: " + data.decode())
                    connection.sendall("All files were sent!".encode())
                    print("Sent: All files were sent!")
                else:
                    break
        finally:
            connection.close()
            exit()  # exit the program otherwise "return CheckResult.correct()" will return a timeout error



if __name__ == '__main__':
    main()