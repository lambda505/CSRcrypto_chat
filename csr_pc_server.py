"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#---Init constant
clients = {}
addresses = {}
HOST = str(input("HOST: "))
PORT = input("PORT: ")
if not PORT:
    PORT = 30000
else:
    PORT = int(PORT)

BUFSIZ = 2048
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#---Methods
def accept_incoming_connections():
    #Sets up handling for incoming clients
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} has connected.")
        #client.send(bytes("Welcome, "+
        #                  "Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    #Handles a single client connection."""
    name = client.recv(BUFSIZ)#.decode("utf8")
    #welcome = f'Welcome {name}' + '! If you ever want to quit, type {quit} to exit.'
    #client.send(bytes(welcome, "utf8"))
    #msg = f"{name} has joined the chat!"
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            #msg = msg[2:-1]
            broadcast(msg)
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                #broadcast(bytes(f"{name} has left the chat.", "utf8"))
            except:
                print("Something went wrong")
            break

def broadcast(msg):  # prefix is for name identification.
    #Broadcasts a message to all the clients.
    err = False
    for sock in clients:
        try:
            print(msg)
            sock.send(msg)
        except:
            print(f"something went wrong with {sock}\nWill delete it")
            print("Oh fuck someone crashed on server side, don't worry i'll erase this mofo")
            #broadcast(bytes(msg, "utf8"))
            err = True
            i = sock
    if err:
        del clients[i]

#---RUN
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()