import sys
import socket

class Server:
    def __init__(self,hostname,port):
        

    #def Run(self,port):
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
            self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.sock.bind(('',port))
            self.sock.listen()	
            print ("socket is listening")
            
            request, clientAddr = self.sock.accept()
            self.sock.close()
            print ('Got connection from', clientAddr)
            request.send('Thank you for connecting'.encode())
            try:
                while request:
                    expression = request.recv(1024)
                    if not expression:
                        print('Client ',clientAddr,' has disconnected')
                        break
                    else:
                        try:
                            print("Query received = ",expression.decode(),' by ',clientAddr)
                            result = eval(expression)
                            request.sendall(str(result).encode())      #converting int to string to byte object 
                        except (SyntaxError, NameError):
                            request.sendall(b'Wrong Expression!')
                            pass
            except socket.error:
                print('Connection closed')
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
   
