import socket
import threading

HOST = "10.0.0.20"
PORT = 8123

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}: {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat.")
            break

def recive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("utf-8"))
        
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client: {nickname}")
        broadcast(f"{nickname} connected to the server! \n".encode("utf-8"))
        client.send("Succesfully connected to the server!".encode("utf-8"))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("Server running")
recive()
