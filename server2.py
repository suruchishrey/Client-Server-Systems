import socket
import threading
import sys

#Variables for holding information about connections
connections = []
total_connections = 0

class Server:
    def __init__(self,hostname,port):
        #Create new server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((hostname, port))
        self.sock.listen(5)
        print ("socket is listening")

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        try:
            while self.signal:
                try:
                    expression = self.socket.recv(1024)
                except:
                    print("Client " + str(self.address) + " has disconnected")
                    self.signal = False
                    connections.remove(self)
                    break
                if expression != "":
                    print("ID " + str(self.id) + ": " + str(expression.decode("utf-8")))
                    for client in connections:
                        if client.id == self.id:
                            if not expression:
                                print("Client " + str(self.address) + " has disconnected")
                                self.signal = False
                                connections.remove(self)
                            #    print('Bye')
                            else:
                                try:
                                    print("Query received = ",expression.decode(),' by ',self.address)
                                    result = eval(expression)
                                    client.socket.send(str(result).encode())      #converting int to string to byte object 
                                except (SyntaxError, NameError):
                                    client.socket.send(b'Wrong Expression!')
                                    pass
                            #client.socket.sendall(data)
        except socket.error:
            print('Connection closed')
            pass

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        sock.send('Thank you for connecting'.encode())
        total_connections += 1

if __name__ == "__main__":
    #Get host and port
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    #Create new server socket
    try:
        server = Server(hostname,port)
    except :
        print('Server not created')
        sys.exit(1)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (server.sock,))
    newConnectionsThread.start()
    