import socket
import threading

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
server_address = ('localhost', 12345)
sock.connect(server_address)

# prompt the user for their username and password
username = input('Enter your username: ')
password = input('Enter your password: ')

# send the username and password to the server
sock.sendall(username.encode())
sock.sendall(password.encode())

# function to receive messages from the server
def receive_messages():
    authenticated = False

    while True:
        try:
            # receive a message from the server
            message = sock.recv(1024).decode()

            # check if the client has been authenticated
            if not authenticated:
                # if the server sends a welcome message, set authenticated to True
                if message.startswith('Welcome'):
                    authenticated = True
                else:
                    # if the server sends an error message, print it and close the socket
                    print(message)
                    sock.close()
                    break
            else:
                # if the client has been authenticated, print messages from the server
                print(message)

        except:
            # if an error occurs, close the socket and break out of the loop
            sock.close()
            break

# start a new thread to receive messages from the server
thread = threading.Thread(target=receive_messages)
thread.start()

# enter a loop to send messages to the server
while True:
    message = input(':> ')
    sock.sendall(message.encode())
