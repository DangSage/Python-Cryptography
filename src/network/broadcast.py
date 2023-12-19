import socket
import json
import time
import traceback
from utility import list_data, verify_token
import nglobals as ng
import globals as gl
from .ndata import control_flow, clear_user_lists
from .tcp import tcp_client


def broadcast_listen(sock):
    '''
    listen for broadcast messages from other users on the network at clients broadcast port
    '''
    
    print("Listening for broadcast from socket", sock.getsockname())
    last_received = {}
    contact_emails = [contact["email"] for contact in gl.CONTACTS]
    sock.settimeout(1)

    message_limit = 500 # messages/second
    counter = 0
    start_time = time.time()
    clients_to_users = {}

    while not ng.stop_threads.is_set():
        try:
            data, addr = sock.recvfrom(4096)
            counter, start_time = control_flow(message_limit, counter, start_time)

            data = json.loads(data.decode())  # Parse the data as JSON
            if data['email'] in ng.online_users and not verify_token(data['email'], data['session_token']):
                print(f"Session token mismatch for user {data['email']}")
                continue

            last_received[addr] = time.time()  # Update the last received time
            user_info = {'email': data['email'], 'tcp': data['tcp'], 'udp': data['udp'], 'addr': addr}
            ng.online_users[data['username']] = user_info

            clients_to_users = {details['addr']: user for user, details in ng.online_users.items()}

            if data['email'] in contact_emails and data['username'] not in ng.online_contacts:
                ng.online_contacts[data['username']] = user_info
                print(f"Contact '{data['username']}' is online")

        except socket.timeout:  # Normal inactivity, check if some clients have disconnected
            current_time = time.time()
            disconnected_clients = [client for client, last_time in last_received.items() if current_time - last_time > 4]

            for client in disconnected_clients:
                if client in clients_to_users:
                    print(f"{clients_to_users.get(client)} disconnected")
                    last_received.pop(client, None)
                    clear_user_lists(clients_to_users.get(client))
            continue
        except json.JSONDecodeError:
            print("Invalid JSON data received: ", data)
            continue
        except (IndexError, KeyError, TypeError):
            last_received[addr] = time.time()
            continue
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            break  # Stop the loop if an error occurs
    sock.close()
    print(" ├─Broadcast listener closed")


def broadcast_send(port):
    '''
    send broadcast message to all users on the network
    '''
    my_info = list_data()
    my_info['session_token'] = ng.session_token
    my_info = json.dumps(my_info)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while not ng.stop_threads.is_set():
        if port != ng.bcast_port:
            s.sendto(my_info.encode(), ("localhost", port))
        port = 1337 if port >= 2000 else port + 1

    # Send a disconnect message to all users
    for user in ng.online_users:
        tcp_client(ng.online_users[user]['tcp'], my_info, "disconnect")
    s.close()
    print(" ├─Broadcast sender closed")