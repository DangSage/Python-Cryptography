import ssl
import datetime
import time
import json
import socket
import nglobals as ng
import globals as gl
from socketserver import BaseRequestHandler, TCPServer
from .ndata import (
    clear_user_lists,
    control_flow,
    parse_user_data,
    user_name_of_email, 
    verify_user, 
    verify_timestamp,
    verify_contact_req
)
from utility import *
import traceback

online_users = ng.online_users


class tcp_handler(BaseRequestHandler):
    def handle(self):
        ''' Main handler for all TCP connections (in) '''
        counter = 0
        start_time = time.time()
        message_limit = 50 # messages per second
        try:
            self.data = self.request.recv(1024).decode()
            counter, start_time = control_flow(message_limit, counter, start_time)
            action, data, timestamp = json.loads(self.data)
            if not verify_timestamp(timestamp):
                raise IndexError("Invalid timestamp received")
            
            if "FILE" in action:
                self.handle_file_action(action, data)
            elif action == "DISCONNECT_REQ":
                self.handle_disconnect_action(data)
            elif action == "REQUEST_REQ":
                self.handle_request_req_action(data)
            elif action == "ACCEPT_REQ":
                self.handle_accept_req_action(data)
            else:
                self.request.sendall(json.dumps("No").encode())
        except (json.JSONDecodeError, IndexError, KeyError):
            self.request.sendall(json.dumps("Invalid data received").encode())
        except (ValueError, Exception) as e:
            self.request.sendall(json.dumps(["ERROR", str(e)]).encode())
            traceback.print_exc()


    def handle_file_action(self, action, data):
        # Handle file action
        parts = action.split("_")
        __, name, sender_email = parts
        if not verify_contact(sender_email):
            raise Exception("File sender is not a contact, file rejected", sender_email)
        decrypted_data = decrypt_file(data)

        # save file
        with open(f"{gl.DOWNLOAD_DIR}{name}", 'wb') as f:
            f.write(decrypted_data)
        
        listfile = {"File": name, "Size": f"{len(decrypted_data)} bytes", "Path": f"{gl.DOWNLOAD_DIR}{name}"}
        display_list(f"File received from {user_name_of_email(sender_email)}", listfile, "No files received")
        self.request.sendall("File received".encode())


    def handle_disconnect_action(self, data):
        # Handle disconnect action
        username = parse_user_data(data, ng.online_contacts)
        if not username:
            raise Exception("Invalid data received")
        print(f"Contact '{username}' disconnected ({self.client_address[0]}:{self.client_address[1]})")
        # no sendall() here, client will close connection
        clear_user_lists(username)


    def handle_request_req_action(self, data):
        # Handle request request action
        email = parse_user_data(data, ng.contact_requests)
        if not email:
            raise Exception("Invalid data received")

        display_list("Contact request received", {"From": ng.contact_requests}, "No contact requests received")
        self.request.sendall(json.dumps(["REQUEST_ACK", json.dumps(list_data())]).encode())


    def handle_accept_req_action(self, data): # "I've accepted your request"
        # Handle accept request action
        data = json.loads(data)
        if not verify_contact_req(data['email']):
            raise Exception("Invalid data received")
        user = data['username']
        
        ng.online_contacts[user] = ng.out_contact_requests.pop(user, None)
        
        add_contact(data)
        print(f"{user} accepted your request ({self.client_address[0]}:{self.client_address[1]})")
        self.request.sendall(json.dumps(["ACCEPT_ACK", json.dumps(list_data())]).encode())


def stop_tcp_listen():
    ng._tcpserver.shutdown()
    ng._tcpserver.server_close()


def tcp_listen(port):
    host = "localhost"
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cntx.verify_mode = ssl.CERT_REQUIRED
    try:
        cntx.load_verify_locations(cafile="bin/ca.crt")
        cntx.load_cert_chain(ng.CERT, ng.KEY)
    except FileNotFoundError:
        print("Certificate file not found")
        return
    except ssl.SSLError:
        # print the error message
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



def tcp_client(port, data, extra=None, is_file=False):
    ''' Secondary handler for all TCP connections (out) '''
    host_ip = "localhost"
    cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    try:
        cntx.load_verify_locations(cafile="bin/ca.crt")
        cntx.load_cert_chain(certfile=ng.CERT, keyfile=ng.KEY)
        cntx.verify_mode = ssl.CERT_REQUIRED

        with socket.create_connection((host_ip, port)) as s:
            with cntx.wrap_socket(s, server_hostname="localhost") as ssl_s:
                timestamp = datetime.datetime.now().isoformat()
                action = ""
                if not is_file:
                    action = extra.upper()+"_REQ" if extra else ""
                else:
                    name = strip_file_path(extra)
                    print(f"Sending file: {name}")
                    action = f"FILE_{name}_{gl.USER_EMAIL}"
                    receivers_cert = ssl_s.getpeercert(binary_form=True)
                    receivers_pem = ssl.DER_cert_to_PEM_cert(receivers_cert) 
                    data = encrypt_file(data, pub_from_pem(receivers_pem)) # data -> encrypted file

                message = json.dumps([action, data, timestamp])
                ssl_s.sendall(message.encode())

                if action == "DISCONNECT_REQ":
                    return
                print("...")
                received = ssl_s.recv(1024).decode()
        

            # Handle received data
            if received and not is_file:
                received_data = json.loads(received)
                if isinstance(received_data, list) and len(received_data) == 2:
                    action, out_data = received_data

                    parsed_user = parse_user_data(out_data, ng.out_contact_requests if action == "REQUEST_ACK" else ng.online_contacts)
                    if not parsed_user:
                        raise Exception("Invalid data received")
                    if action == "REQUEST_ACK":
                        print(f"Contact request sent to '{parsed_user}'")
                    elif action == "ACCEPT_ACK":
                        ng.contact_requests.pop(parsed_user, None)
                        add_contact(json.loads(out_data))
                        # print contact most recently added
                        display_list("Contact added", ng.online_contacts, "No contacts added")
                else:
                    print("Unexpected data format received")
            elif received and is_file:
                if received == "File received":
                    print("File sent")
                else:
                    print(f"Could not send file: {received}")
    except ConnectionRefusedError:
        if verify_user(port):
            pass    # broadcast listener will handle this
        else:
            print("Connection refused")
    except (FileNotFoundError, ssl.SSLError, json.decoder.JSONDecodeError) as e:
        print(f"{e}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()