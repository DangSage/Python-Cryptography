import ssl
import json
import socket
import base64
import nglobals as ng
import globals as gl
from socketserver import BaseRequestHandler, TCPServer
from .ndata import parse_user_data, user_name_of_email
from utility import *
import traceback

online_users = ng.online_users

class tcp_handler(BaseRequestHandler):
    def handle(self):
        try:
            self.data = self.request.recv(1024).decode()
            action, data = json.loads(self.data)
            if "FILE" in action:
                # get file name
                parts = action.split("_")
                __, name, sender_email = parts
                if not verify_contact(sender_email):
                    raise Exception("File sender is not a contact, file rejected", sender_email)
                print(f"Received from {user_name_of_email(sender_email)}")
                decrypted_data = decrypt_file(data)
                # save file
                with open(f"{gl.DOWNLOAD_DIR}{name}", 'wb') as f:
                    f.write(decrypted_data)
                f.close()
                print(f"File received: {name}")
                self.request.sendall("File received".encode())
            elif action == "REQUEST_REQ":
                username = parse_user_data(data, ng.contact_requests)
                if not username:
                    raise Exception("Invalid data received")
                print(f"Contact request received from '{username}'({self.client_address[0]})")
                self.request.sendall(json.dumps(["REQUEST_ACK", list_data()]).encode())

            elif action == "ACCEPT_REQ":
                username = parse_user_data(data, ng.out_contact_requests)
                ng.online_contacts[username] = ng.out_contact_requests.pop(username, None)
                add_contact(gl.USER_EMAIL, [username, ng.online_contacts[username][0]])
                print(f"Accepted '{username}'s' Request ({self.client_address[0]}:{self.client_address[1]})")
                self.request.sendall(json.dumps(["ACCEPT_ACK", list_data()]).encode())

            elif action == "":
                self.request.sendall(json.dumps("No").encode())
            else:
                self.request.sendall(json.dumps("ping").encode())
        except json.JSONDecodeError:
            self.request.sendall(json.dumps("Invalid data received").encode())
        except (ValueError, Exception) as e:
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
        stop_tcp_listen()
        print(" ├─TCP listener closed")


def tcp_client(port, data, action=None, is_file=False):
    host_ip = "localhost"
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    try:
        cntx.load_verify_locations(cafile="bin/ca.crt")
        cntx.load_cert_chain(certfile=ng.CERT, keyfile=ng.KEY)
        cntx.verify_mode = ssl.CERT_REQUIRED

        with socket.create_connection((host_ip, port)) as s:
            with cntx.wrap_socket(s, server_hostname="localhost") as ssl_s:
                if not is_file:
                    message = json.dumps([f"{action.upper()}_REQ" if action else "", data])
                else:
                    name = strip_file_path(action)
                    print(f"Sending file: {name}")
                    receivers_cert = ssl_s.getpeercert(binary_form=True)
                    receivers_pem = ssl.DER_cert_to_PEM_cert(receivers_cert) 
                    encrypted_file_info = encrypt_file(data, pub_from_pem(receivers_pem))
                    message = json.dumps([f"FILE_{name}_{gl.USER_EMAIL}", encrypted_file_info])
                print("...")
                ssl_s.sendall(message.encode())
                received = ssl_s.recv(1024).decode()
        
        if received and not is_file:
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
                    add_contact(gl.USER_EMAIL, [parsed_user, ng.online_contacts[parsed_user][0]])
                    print(f"'{parsed_user}' accepted your contact request")
            elif isinstance(json.loads(received), str):
                message = json.loads(received)
            else:
                print("Unexpected data format received")
                return
            
        elif received and is_file:
            if received == "File received":
                print("File sent")
            else:
                print(f"Could not send file: {received}")
    except (FileNotFoundError, ssl.SSLError, ConnectionRefusedError, json.decoder.JSONDecodeError, Exception) as e:
        print(f"Error: {e}")
        traceback.print_exc()