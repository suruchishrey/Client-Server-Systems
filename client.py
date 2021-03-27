import socket
import select
import sys


def prompt():
    sys.stdout.write("> ")
    sys.stdout.flush()


class Client(object):
    def __init__(self):
        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.sock = None
        self.connect_to_server()

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        # connect to remote host
        try:
            self.sock.connect((self.host, self.port))
        except:
            print ('Connection Refused! Unable to connect')
            sys.exit()

        print('Connected to remote host. Start sending arithmetic queries.')
        data = self.sock.recv(1024)
        sys.stdout.write(data.decode()+'\n')
        prompt()
        self.wait_for_messages()

    def wait_for_messages(self):
        try:
            while True:
                # user entered a message
                msg = sys.stdin.readline()
                self.sock.send(msg.encode())
                prompt()
                # incoming message from remote server
                data = self.sock.recv(1024)
                if not data:
                    print ('\nDisconnected from server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write('Server replied: '+data.decode()+'\n')
                    prompt()
        except socket.error:
            print('\nDisconnected from server')

                
 
                    


if __name__ == '__main__':
    client = Client()