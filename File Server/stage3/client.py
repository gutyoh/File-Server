import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("127.0.0.1", 12345)
sock.connect(server_address)
print("Client started!")

try:
    # Send data
    message = "Give me everything you have!"
    print("Sent: " + message)
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len("All files were sent!")

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print("Received: " + data.decode())

finally:
    sock.close()
    exit()  # exit the program otherwise "return CheckResult.correct()" will return a timeout error
