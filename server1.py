import sys
import socket

BUFFER_SIZE = 1024

class Server:
    def __init__(self,hostname,port):

        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Create and return a new socket object to use IP v4 and TCP.
            self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  #Set options on the socket.socket.SO_REUSEADDR, causes the port to be released immediately after the socket is closed
            self.sock.bind((hostname,port))         # bind host address and port together
            # put the socket into listening mode
            self.sock.listen()	
            print ("socket is listening")

             # Establish connection with client.
            request, clientAddr = self.sock.accept()
            self.sock.close()               #closing the socket's inputstream and outputstream so that now it cannot be connected to any other client
            print ('Got connection from', clientAddr)
            request.send('Thank you for connecting'.encode())
            try:
                while request:
                    # receive data stream. it won't accept data packet greater than 1024 bytes
                    expression = request.recv(BUFFER_SIZE)
                    if not expression:
                        # if data is not received break and close the socket
                        print('Client ',clientAddr,' has disconnected')
                        request.close()
                        break
                    else:
                        try:
                            print("Query received = ",expression.decode(),' by ',clientAddr)
                            result = eval(expression)
                            # send data to the client
                            request.send(str(result).encode())      #converting int to string to byte object 
                        except (SyntaxError, NameError, ZeroDivisionError):
                            request.send(b'Wrong Expression!')
                            pass
                        except :
                            request.send(b'Wrong Expression!')
                            pass
            except socket.error:
                print('Connection closed')
                request.close()
                pass

if __name__ == "__main__":
    if len(sys.argv)<3:
        print('Enter %s [hostname] [portnumber]'%sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    try:
        server = Server(hostname,port)
    except :
        print('Server not created')
        sys.exit(1)
   
