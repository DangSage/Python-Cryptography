import socket
from time import sleep
from utility import (
    get_user_name_from_list,
    check_contacts
)
import globals as gl
import nglobals as ng
from .tcp import tcp_client

import traceback

def broadcast_listen(socket, shutdown_event):
    print("Listening for broadcast from socket ", socket.getsockname())
    socket.settimeout(1)  # Set a timeout
    try:
        while not shutdown_event.is_set():
            try:
                data = socket.recvfrom(4096)
            except TimeoutError:
                continue
            data = eval(data[0])
            # code to check if in contacts
            email_exists = check_contacts(data)
            ng.potential_contact = data
            # send back a yes if in contacts, with information back
            if ng.potential_contact[3] not in ng.ignore_bcast_port:
                list = (
                    get_user_name_from_list(),
                    gl.USER_EMAIL,
                    ng.tcp_listen,
                    ng.bcast_port,
                )
                ls = str(list)
                tcp_client(data[2], ls)
    except Exception as e:
        print(f"Error in broadcast_listener: {e}")
        traceback.print_exc()
    finally:
        socket.close()
        print("Broadcast listener closed")


def broadcast_send(port, shutdown_event):
    list = (get_user_name_from_list(), gl.USER_EMAIL, ng.tcp_listen, ng.bcast_port)
    msg = str(list)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while not shutdown_event.is_set():
            if port != ng.bcast_port:
                s.sendto(msg.encode(), ("localhost", port))
            if port >= 2000:
                port = 1337
            elif port != 2000:
                port += 1
            sleep(0.01)  # goes through all the ports in about a minute
    except:
        pass
    finally:
        s.close()
        print("Broadcast sender closed")