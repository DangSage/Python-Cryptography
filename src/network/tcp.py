import ssl
import json
import socket
import nglobals as ng
import globals as gl
from socketserver import BaseRequestHandler, TCPServer
from .ndata import parse_user_data, verify_contact_req, verify_user
from utility import list_data, add_contact
import traceback

online_users = ng.online_users


class tcp_handler(BaseRequestHandler):
    def handle(self):
        try:
            self.data = self.request.recv(1024).decode()
            action, data = json.loads(self.data)
            if action == "REQUEST_CONTACT":
                parsed_user = parse_user_data(data, ng.contact_requests)
                if not parsed_user:
                    raise Exception("Invalid data received")
                print(f"Contact request received from '{parsed_user}'({self.client_address[0]}:{self.client_address[1]})")
                self.request.sendall(json.dumps(["REQUEST_ACK", list_data()]).encode())
            elif action == "ACCEPT_CONTACT":
                # would only be getting this if this client sent a request
                parsed_user = parse_user_data(data, ng.out_contact_requests)
                ng.online_contacts[parsed_user] = ng.out_contact_requests.pop(parsed_user, None)
                add_contact(gl.USER_EMAIL, [parsed_user, ng.online_contacts[parsed_user][0]])
                print(f"Contact request accepted from '{parsed_user}'({self.client_address[0]}:{self.client_address[1]})")
                self.request.sendall(json.dumps(["ACCEPT_ACK", list_data()]).encode())
            elif action == "":
                # send no back to client
                self.request.sendall(json.dumps("No").encode())
            else:
                # message
                self.request.sendall(json.dumps("ping").encode())
        except json.decoder.JSONDecodeError:
            print("Invalid JSON data received" + self.client_address[0])
            return None
        except Exception as e:
            self.request.sendall(json.dumps(["ERROR", str(e)]).encode())
            traceback.print_exc()


def stop_tcp_listen():
    ng._tcpserver.shutdown()
    ng._tcpserver.server_close()


def tcp_listen(port):
    host = ""
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cntx.verify_mode = ssl.CERT_REQUIRED
    try:
        cntx.load_verify_locations(cafile="bin/ca.crt")
        cntx.load_cert_chain(ng.CERT, ng.KEY)
    except FileNotFoundError:
        print("Certificate file not found")
        return
    except ssl.SSLError:
        print("Invalid certificate file")
        return

    ng._tcpserver = TCPServer((host, port), tcp_handler)
    ng._tcpserver.socket = cntx.wrap_socket(ng._tcpserver.socket, server_side=True)
    try:
        ng._tcpserver.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        ng._tcpserver.shutdown()
        ng._tcpserver.server_close()
        print("TCP listener closed")


def tcp_client(port, data, action=None, is_file=False):
    host_ip = "localhost"
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try:
        cntx.load_verify_locations(cafile="bin/ca.crt")
        cntx.load_cert_chain(certfile=ng.CERT, keyfile=ng.KEY)
        with socket.create_connection((host_ip, port)) as s:
            with cntx.wrap_socket(s, server_hostname="localhost") as ssl_s:
                if not is_file:
                    message = json.dumps([f"{action.upper()}_REQ" if action else "", data])
                    ssl_s.sendall(message.encode())
                else:
                    ssl_s.sendall(data)
                received = ssl_s.recv(1024).decode()
        
        # wait for response from receiver
        if received:
            if isinstance(json.loads(received), list) and len(json.loads(received)) == 2:
                action, out_data = json.loads(received)
                if action == "REQUEST_ACK":
                    parsed_user = parse_user_data(out_data, ng.out_contact_requests)
                    if not parsed_user:
                        raise Exception("Invalid data received")
                    print(f"Contact request sent to '{parsed_user}'")
                elif action == "ACCEPT_ACK":
                    parsed_user = parse_user_data(out_data, ng.online_contacts)
                    if not parsed_user:
                        raise Exception("Invalid data received")
                    ng.online_contacts[parsed_user] = ng.contact_requests.pop(parsed_user, None)
                    
                    # write contact to file
                    add_contact(gl.USER_EMAIL, [parsed_user, ng.online_contacts[parsed_user][0]])
                    print(f"'{parsed_user}' accepted your contact request")
            elif isinstance(json.loads(received), str):
                message = json.loads(received)
            else:
                print("Unexpected data format received")
                    
    except (FileNotFoundError, ssl.SSLError):
        print("Certificate file not found or invalid")
    except ConnectionRefusedError:
        print(f"Connection refused by {host_ip}:{port}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON data received from {host_ip}:{port}\n\t{received}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

        