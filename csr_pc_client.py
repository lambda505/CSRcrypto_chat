"""Script for Tkinter GUI chat client."""
import time
import os
import tkinter
import rsa
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

#---Methods
class encryption:
    def get_pubkey(path):
        # Setup the Public key to send a msg to someone
        pkey = open(path, 'rb')
        pkdata = pkey.read()
        pubkey = rsa.PublicKey.load_pkcs1(pkdata)
        return pubkey

    def get_privkey(path):
        # Setup Private key in case you use other's private key to decrypt
        pkey = open(path, 'rb')
        pkdata = pkey.read()
        privkey = rsa.PrivateKey.load_pkcs1(pkdata)
        return privkey

    def encrypt(message, pubkey):
        # Encrypt message
        crypto = rsa.encrypt(message, pubkey)
        return crypto

    def decrypt(message, privkey):
        # Descrypt message
        decrypt = rsa.decrypt(message, privkey)
        return decrypt

#Fake init
dir_path = os.path.dirname(os.path.realpath(__file__))
publickey = encryption.get_pubkey(dir_path + "\\keys\\_publickey.key")
privatekey = encryption.get_privkey(dir_path + "\\keys\\_privatekey.key")

print("---TEST---")
msg = encryption.encrypt(bytes("Testing encryption", "utf-8"), publickey)
print(f"Encrypted:\n{msg}")
msg = encryption.decrypt(msg, privatekey)
print(f"Decrypted:\n{msg}")
print("------------------")

class chat:
    def receive():
        #Handles receiving of messages
        while True:
            try:
                msg = client_socket.recv(BUFSIZ)#.decode("utf8")
                if msg != bytes("{quit}", "utf8"):
                    try:
                        global privatekey
                        print('\nReceived')
                        print(msg)
                        print("-----------------------")
                        msg = encryption.decrypt(msg, privatekey)
                        print(msg)
                    except:
                        msg = f"Couldnt decrypt {msg}"
                msg_list.insert(tkinter.END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(event=None):  # event is passed by binders(tkinter).
        #Handles sending of messages
        msg = my_msg.get()
        if msg != "{quit}":
            global publickey
            print('\nSended')
            msg = f"{username}: {msg}"
            print(msg)
            msg = encryption.encrypt(bytes(msg, "utf8"), publickey)
            print(msg)
        else:
            # Encode quit command to be readable by the server
            msg = bytes('{quit}', 'utf-8')
        my_msg.set("")  # Clears input field.
        print("--------------------")
        print(msg)
        client_socket.send(msg)
        if msg == bytes('{quit}', 'utf-8'):
            client_socket.close()
            time.sleep(3)
            top.quit()

    def on_closing(event=None):
        #This function is to be called when the window is closed
        my_msg.set("{quit}")
        chat.send()


#---Init window
top = tkinter.Tk()
top.title("CSR Private Chat")
#
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
#Define message list that will go in message_frame
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

#Define the text writing zone for sending
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", chat.send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=chat.send)
send_button.pack()
#
top.protocol("WM_DELETE_WINDOW", chat.on_closing)

#---CONSTANT
HOST = askstring('HOST', 'Enter host adress: ')
PORT = askstring('PORT', 'Enter port (empty for default): ')
showinfo('Trying to join', '{}'.format(HOST))
if not HOST:
    HOST = "127.0.0.1"  # Default value.
else:
    pass
if not PORT:
    PORT = 30000  # Default value.
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect_ex(ADDR)

#RSA KEYS
path_pubkey = askstring('PUBKEY', 'Enter Public Key full path: ')
if not path_pubkey:
    pass
else:
    publickey = encryption.get_pubkey(path_pubkey)
#
path_privkey = askstring('PRIVKEY', 'Enter Private Key full path: ')
if not path_privkey:
    pass
else:
    privatekey = encryption.get_privkey(path_privkey)

username = askstring('USERNAME', 'Choose a username: ')
chat.send(username)

#---RUN
receive_thread = Thread(target=chat.receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
