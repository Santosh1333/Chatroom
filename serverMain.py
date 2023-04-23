import socket
import threading

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific IP address and port
server_address = ('localhost', 12345)
sock.bind(server_address)

# listen for incoming connections
sock.listen(5)
print('Server started')

# list of connected clients
clients = []

# function to handle incoming messages from a client
def handle_client(client_socket, client_address):
    # receive the username and password from the client
    username = client_socket.recv(1024).decode()
    password = client_socket.recv(1024).decode()

    # check if the username and password are valid
    # (you'll need to implement your own authentication mechanism)
    if username == 'admin' and password == 'password':
        # add the client to the list of connected clients
        clients.append(client_socket)

        # send a welcome message to the client
        client_socket.sendall('Welcome to the chatroom!'.encode())

        # broadcast the client's username to all other clients
        message = '{} has joined the chat'.format(username)
        broadcast(message, client_socket)

        # enter a loop to receive messages from the client
        while True:
            try:
                # receive a message from the client
                message = client_socket.recv(1024).decode()

                # broadcast the message to all other clients
                broadcast('{}: {}'.format(username, message), client_socket)

            except:
                # if an error occurs, remove the client from the list of connected clients
                clients.remove(client_socket)

                # broadcast a message to all other clients
                message = '{} has left the chat'.format(username)
                broadcast(message, client_socket)

                # close the socket
                client_socket.close()

                # break out of the loop
                break

    else:
        # if the username and password are invalid, send an error message to the client
        client_socket.sendall('Invalid username or password'.encode())
        client_socket.close()

# function to broadcast a message to all clients except the sender
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)
                client.close()

# enter a loop to accept incoming connections from clients
while True:
    # accept a connection from a client
    client_socket, client_address = sock.accept()

    # start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
