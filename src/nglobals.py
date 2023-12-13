import socket
import subprocess
import os

own_ip = None
potential_contact = ()
ignore_bcast_port = []

CERT = ""
KEY = ""

bcast_port = 1337   # temp port_manager(1377, 9900)
tcp_listen = 9900   # temp port_manager(1377, 9900)
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


