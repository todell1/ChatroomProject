import socket 
import threading


# Connection Information
host = socket.gethostbyname(socket.gethostname())
port = 55555

# Starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List for Clients and their names 
clients = []
nicknames = []

# Sending messages to ALL connected clients
def broadcast(msg):
    for client in clients:
        client.send(msg)
        
# Handing messages from the clients 
def handle(client):
    connected = True 
    while connected:
        try: 
            #Broadcast the message
            msg = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {msg}")
            broadcast(msg)
        except:
            # Removing and closing the clients 
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = nicknames[index]
            broadcast('{} left!'.format(name).encode('ascii'))
            nicknames.remove(name)
            break 
        
# Receiving and Listening Function 
def receive():
    while True:
        # Accept the connection
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        # Request and store name
        client.send('NAME'.encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        # Print and broadcast name 
        print("Name is {}".format(nickname))
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))
        # Start handling thread for client 
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server running .....")       
receive()
    

        

