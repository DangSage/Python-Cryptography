import socket
import subprocess
import os

own_ip = None
potential_contact = ()
ignore_bcast_port = []

CERT = ""
KEY = ""

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
            print(f"Port {lport} is already in use.")
            bport += 1
            lport += 1
            attempts += 1
    print("Could not find an open port.")
    return None, None

bcast_port, tcp_listen = port_manager(1377, 9900)
tcp_port = 9900


def gen_certificate(user_info):
    global CERT, KEY
    # if windows, run the windows script
    if os.name == "nt":
        subprocess.run(["bin\\client_certs.bat", user_info], capture_output=True, text=True)
    else:
        subprocess.run(["./bin/client_certs.sh", user_info], capture_output=True, text=True)
    CERT = "bin/certs/client_"+user_info+'/' + user_info + "cert.crt"
    KEY = "bin/certs/client_"+user_info+'/' + user_info + "key.pem"


