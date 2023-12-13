import ssl
import socket
from socketserver import BaseRequestHandler, TCPServer
from utility import contacts_dict_exist
from utility import check_contacts
import globals as gl
import nglobals as ng

CERT = ng.CERT
KEY = ng.KEY
potential_contact = ng.potential_contact
ignore_bcast_port = ng.ignore_bcast_port

server = None

class tcp_handler(BaseRequestHandler):
    def handle(self):
        """
        This function is what can handle whether or not the sender is a contact
        """
        self.data = self.request.recv(1024).strip()
        try:
            if type(eval(self.data)) is tuple:
                if contacts_dict_exist():
                    self.data = eval(self.data)
                    print(self.data)
                    email_exists = check_contacts(self.data)
                    if email_exists:
                        self.request.sendall("Yes".encode())
                    elif not email_exists:
                        self.request.sendall("No".encode())
                else:
                    self.request.sendall("No".encode())
        except SyntaxError:
            confirmation = input(f"Contact <____> is sending a file. Accept (y/n)?")

            if confirmation == 'y' or confirmation == 'Y':
                f = open("recieved_file", "wb")
                f.write(self.data)
                running = True
                while running:
                    print("hang up in handle")
                    self.data = self.request.recv(1024)
                    if not self.data:
                        break
                    if self.data.decode() == "stop":
                        running = False
                        break
                    f.write(self.data)
                f.close()
                self.request.sendall("AWK from server".encode())
            else:
                print("File not accepted\n")
        # self.request.sendall("AWK from server".encode())


def stop_tcp_listener():
    global server
    server.shutdown()
    server.server_close()


def tcp_listener(port):
    global server
    host = ""
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cntx.load_cert_chain(CERT, KEY)

    server = TCPServer((host, port), tcp_handler)
    server.socket = cntx.wrap_socket(server.socket, server_side=True)
    try:
        server.serve_forever()
    except:
        pass
    finally:
        server.server_close()
        print("TCP listener closed")


def tcp_client(port, data, is_file=False):
    host_ip = "localhost"

    # Initialize a TCP client socket using SOCK_STREAM
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    cntx.load_verify_locations(CERT)
    cntx.load_cert_chain(CERT, KEY)

    s = cntx.wrap_socket(s, server_hostname="test.server")

    if not is_file:
        try:
            # Establish connection to TCP server and exchange data
            s.connect((host_ip, port))
            s.sendall(data.encode())
            # Read data from the TCP server and close the connection
            recieved = s.recv(1024)
        finally:
            s.close()
    elif is_file:
        try:
            try:
                with open(data, 'rb') as f:

                    f = open(data, "rb")
                    s.connect((host_ip, port))
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        print("Sent ", repr(l))
                        l = f.read(1024)
                    s.sendall("stop".encode())
                    recieved = s.recv(1024)
            except IOError as e:
                print(f"Could not open the file you want to trasnfer {e}")
                print(f"\tMake sure the file path is correct")
        finally:
            # s.send("stop")
            f.close()
            s.close()

    if recieved.decode() == "Yes":
        if potential_contact not in gl.ONLINE_CONTACTS:
            gl.ONLINE_CONTACTS.append(potential_contact)
            ignore_bcast_port.append(potential_contact[3])
    elif recieved.decode() == "No":
        pass
    else:
        pass
    