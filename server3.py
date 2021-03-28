import socket
import select
import sys


class Server:
    # List to keep track of socket descriptors(basically list containing the input sources)
    CONNECTION_LIST = []

    def __init__(self,hostname,port):
        self.user_name_dict = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_up_connections()
        self.client_connect()

    def set_up_connections(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((hostname, port))
        self.server_socket.listen()  
        print('socket is listening')
        # Add server socket to the list of readable connections
        self.CONNECTION_LIST.append(self.server_socket)

    def setup_connection(self):
        sockfd, addr = self.server_socket.accept()
        self.CONNECTION_LIST.append(sockfd)
        print ("Client (%s, %s) connected" % addr)
        self.send_data_to(sockfd, "Thank you for connecting\n Enter query: ")
        self.user_name_dict.update({sockfd: Client(addr)})                      # Use of Client class


    def send_data_to(self, sock, message):
        try:
            sock.send(message.encode())
        except:
            # broken socket connection may be, chat client pressed ctrl+c for example
            sock.close()
            print("msg couldnot be sent")
            self.CONNECTION_LIST.remove(sock)

    def client_connect(self):
        print ("Server started on port ",str(port))
        while True:
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])

            for sock in read_sockets:
                # New connection
                if sock == self.server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    self.setup_connection()

                # Some incoming message from a client
                else:
                    # Data received from client, process it
                    try:
                        expression = sock.recv(1024)
                        if expression:
                            print('Query received =',expression.decode(),'by (%s, %s)'%self.user_name_dict[sock].address)
                    
                            try:
                                result = eval(expression)
                                self.send_data_to(sock,str(result))      #converting int to string to byte object 
                            except (SyntaxError, NameError):
                                self.send_data_to(sock,'Wrong Expression!')
                                pass
                            except :
                                self.send_data_to(sock,'Wrong Expression!')
                                pass
                        else:
                            print("Client (%s, %s) has disconnected" %self.user_name_dict[sock].address)
                            sock.close()
                            self.CONNECTION_LIST.remove(sock)
                    except:
                        
                        print ("Client (%s, %s) is offline" %self.user_name_dict[sock].address)
                        sock.close()
                        self.CONNECTION_LIST.remove(sock)

class Client(object):
    def __init__(self, address):
        self.address = address
        self.name = None


if __name__ == "__main__":
    if len(sys.argv)<3:
        print('Enter %s [hostname] [portnumber]'%sys.argv[0])
        sys.exit(1)
    #Get host and port
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    #Create new server socket
    try:
        server = Server(hostname,port)
    except :
        print('Server not created')
        sys.exit(1)