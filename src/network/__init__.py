import socket
from time import sleep
from threading import Thread, Event
import globals as gl
import nglobals as ng
from .broadcast import *
from .tcp import *

shutdown_event = Event()

def network_manager():
    ng.gen_certificate(gl.USER_EMAIL)

    # broadcast to other users that you exist
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.bind(("", ng.bcast_port))
    

    _broadcast_listener = Thread(
        target=broadcast_listener,
        name="broadcast_listener",
        args=(broadcast_socket, shutdown_event,)
    )

    _broadcast_sender = Thread(
        target=broadcast_sender,
        name="broadcast_sender",
        args=(ng.bcast_port, shutdown_event,)
    )

    _tcp_listener = Thread(
        target=tcp_listener,
        name="tcp_listener",
        args=(ng.tcp_listen,)
    )

    procs = [
        _broadcast_listener,
        _broadcast_sender,
        _tcp_listener
    ]

    try:
        for p in procs:
            p.start()
        while any(p.is_alive() for p in procs) and not shutdown_event.is_set():
            sleep(0.1)  # Check every 100 ms
    except:
        shutdown_event.set()
        if(_tcp_listener.is_alive()):
            stop_tcp_listener()
    for p in procs:
        p.join()