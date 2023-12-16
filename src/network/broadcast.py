import socket
import json
import time
from utility import list_data
import nglobals as ng
import globals as gl
from .tcp import tcp_client


def broadcast_listen(sock, shutdown_event):
    print("Listening for broadcast from socket", sock.getsockname())
    last_received = {}
    contact_emails = [contact["email"] for contact in gl.CONTACTS]
    sock.settimeout(1)
    while not shutdown_event.is_set():
        try:
            clients_to_users = {details[3]: user for user, details in ng.online_users.items()}

            data, addr = sock.recvfrom(4096)
            data = json.loads(data.decode())  # Parse the data as JSON
            last_received[addr] = time.time()  # Update the last received time
            user_info = [data[1], data[2], data[3], addr]
            ng.online_users[data[0]] = user_info

            if data[1] in contact_emails and data[0] not in ng.online_contacts:
                ng.online_contacts[data[0]] = user_info
                print(f"Contact '{data[0]}' is online")

        except socket.timeout:
            current_time = time.time()
            disconnected_clients = [client for client, last_time in last_received.items() if current_time - last_time > 4]
            for client in disconnected_clients:
                print(f"{clients_to_users.get(client)} disconnected")
                last_received.pop(client)
                ng.online_users.pop(client, None)
                ng.online_contacts.pop(client, None)
            continue
                        
        except Exception as e:
            print(f"Error in broadcast_listener: {e}")
            break  # Stop the loop if an error occurs
    sock.close()
    print("Broadcast listener closed")


def broadcast_send(port, shutdown_event):
    my_info = list_data()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        while not shutdown_event.is_set():
            if shutdown_event.is_set():
                    break
            if port != ng.bcast_port:
                s.sendto(my_info.encode(), ('<broadcast>', port))
            port = 1337 if port >= 2000 else port + 1
    except:
        pass
    finally:
        # Send a disconnect message to all users
        for user in ng.online_users:
            tcp_client(ng.online_users[user][2], my_info, "disconnect")
        s.close()
        print("Broadcast sender closed")