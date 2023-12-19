from threading import Event

own_ip = None

session_token = None

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

stop_threads = Event()


CERT = ""
KEY = ""

bcast_port = 1337   # temp port_manager(1377, 9900)
tcp_listen = 9900   # temp port_manager(1377, 9900)
tcp_port = 9900



