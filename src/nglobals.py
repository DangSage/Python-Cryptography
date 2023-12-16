import subprocess
from threading import Event
import os

own_ip = None

online_users = {} 
'''list of online users on the network'''

online_contacts = {} 
'''list of trusted users on the network'''

contact_requests = {} 
'''list of contact requests received by the client'''

out_contact_requests = {} 
'''list of pending contact requests sent by the client'''

ignore_bcast_port = [] 
'''list of ports to ignore when broadcasting'''

_tcpserver = None 
'''TCP server object'''

network_ready = Event()

CERT = ""
KEY = ""

bcast_port = 1337   # temp port_manager(1377, 9900)
tcp_listen = 9900   # temp port_manager(1377, 9900)
tcp_port = 9900


def gen_certificate(user_info):
    '''Generate certificate and key for the user. Is used for all TCP connections'''
    global CERT, KEY
    # if windows, run the windows script
    if os.name == "nt":
        subprocess.run(["bin\\client_certs.bat", user_info], capture_output=True, text=True)
    else:
        subprocess.run(["./bin/client_certs.sh", user_info], capture_output=True, text=True)
    CERT = "bin/certs/client_"+user_info+'/' + user_info + "cert.crt"
    KEY = "bin/certs/client_"+user_info+'/' + user_info + "key.pem"


