import socket
from time import sleep
from threading import Thread
import globals as gl
import nglobals as ng
from .contact import *
from .broadcast import *
from .ndata import *
from .tcp import *

def port_manager(bport, lport, max_attempts=1000):
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    attempts = 0
    # get own ipv4 address
    ng.own_ip = socket.gethostbyname(socket.gethostname())
    while attempts < max_attempts:
        try:
            test_socket.bind(("", bport))
            if bport >= 2000:
                bport = 1337
            test_socket.close()
            return bport, lport
        except OSError:
            bport += 1
            lport += 1
            attempts += 1
    print("Could not find an open port.")
    return None, None


def network_manager():
    session_token()
    gen_certificate(gl.USER_EMAIL)
    ng.bcast_port, ng.tcp_listen = port_manager(ng.bcast_port, ng.tcp_listen)

    # broadcast socket setup (multicast)
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.bind(("", ng.bcast_port))
    

    udp_listener = Thread(
        target=broadcast_listen,
        name="broadcast_listener",
        args=(broadcast_socket,)
    )

    udp_sender = Thread(
        target=broadcast_send,
        name="broadcast_sender",
        args=(ng.bcast_port,)
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
        ng.network_ready.set()
        # while all processes are alive and ng.stop_threads is not set
        while all([p.is_alive() for p in procs]) and not ng.stop_threads.is_set():
            sleep(0.1)  # Check every 100 ms
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ng.stop_threads.set()
        if tcp_listener.is_alive():
            stop_tcp_listen()
        for p in procs:
            p.join()
        print(" └─>Network manager closed\n")
        return