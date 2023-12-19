import os
import signal
import sys
import subprocess
import atexit
import nglobals as ng
import globals as gl
from .data import load_user_data, save_user_data


def handle_sigterm(signum, frame):
    cleanup()
    sys.exit(0)
    

def cleanup():  # not in utility module
    os.remove(ng.KEY)
    os.remove(ng.CERT)
    os.rmdir("bin/certs/client_"+gl.USER_EMAIL)
    
    user_data = load_user_data()
    user_data[gl.USER_EMAIL]["session_token"] = None
    save_user_data(user_data)


def gen_certificate(user_info):
    '''Generate certificate and key for the user. Is used for all TCP connections'''
    bash_path = "C:/Program Files/Git/git-bash.exe"  # Update this if your Git Bash is installed in a different location
    script_path = "./bin/client_certs.sh"
    cmd = []

    if os.name == 'nt':
        cmd = [bash_path, "-c", f"{script_path} {user_info}"]
    else:
        cmd = [script_path, user_info]
    subprocess.run(cmd, capture_output=True, text=True)

    ng.CERT = "bin/certs/client_"+user_info+'/' + user_info + "cert.crt"
    ng.KEY = "bin/certs/client_"+user_info+'/' + user_info + "key.pem"

    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, handle_sigterm)