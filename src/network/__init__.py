import socket
from time import sleep
from threading import Thread, Event
import globals as gl
import nglobals as ng
from .contact import *
from .broadcast import *
from .ndata import *
from .tcp import *

shutdown_event = Event()

def port_manager(bport, lport, max_attempts=1000):
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    attempts = 0
    while attempts < max_attempts:
        try:
            test_socket.bind(("", bport))
            if bport >= 2000:
                bport = 1337
            test_socket.close()
            print(f"Broadcast port: {bport}\nTCP port: {lport}")
            return bport, lport
        except OSError:
            bport += 1
            lport += 1
            attempts += 1
    print("Could not find an open port.")
    ng.own_ip = socket.gethostbyname(socket.gethostname())
    return None, None


def network_manager():
    ng.gen_certificate(gl.USER_EMAIL)
    ng.bcast_port, ng.tcp_listen = port_manager(ng.bcast_port, ng.tcp_listen)

    # broadcast socket setup (multicast)
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.bind(("", ng.bcast_port))
    

    udp_listener = Thread(
        target=broadcast_listen,
        name="broadcast_listener",
        args=(broadcast_socket, shutdown_event,)
    )

    udp_sender = Thread(
        target=broadcast_send,
        name="broadcast_sender",
        args=(ng.bcast_port, shutdown_event,)
    )

    tcp_listener = Thread(
        target=tcp_listen,
        name="tcp_listener",
        args=(ng.tcp_listen,)
    )

    procs = [
        udp_listener,
        udp_sender,
        tcp_listener
    ]

    try:
        for p in procs:
            p.start()
        # while all processes are alive and shutdown_event is not set
        while all([p.is_alive() for p in procs]) and not shutdown_event.is_set():
            sleep(0.1)  # Check every 100 ms
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        shutdown_event.set()
        if tcp_listener.is_alive():
            stop_tcp_listen()
        for p in procs:
            p.join()