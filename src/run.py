import os
from utility import yes_no_prompt, load_user_data
from secure_shell import (
    login_user,
    register_user,
    start_cmd
)
import nglobals as ng
import globals as gl
from network import network_manager
from threading import Thread

def start():
    try:
        if load_user_data() != {}:
            print("Users are registered with this client.\n")
            options = {
                "1": login_user,
                "q": exit,
                "quit": exit,
                "exit": exit,
                "x": exit
            }
            inp = ""
            while inp not in options:
                print("(1) -> Login\n"
                    "(q) -> Quit\n")
                inp = input("Pick an option > ").lower()
            options[inp]()
        else:
            print("No users are registered with this client.\n")
            yes_no_prompt("Do you want to register (y/n)? ", register_user, exit)
    except KeyboardInterrupt:
        exit()

def cleanup():
    os.remove(ng.KEY)
    os.remove(ng.CERT)
    os.rmdir("bin/certs/client_"+gl.USER_EMAIL)

def run():
    start()
    cmd = Thread(target=start_cmd)
    cmd.start()
    network_manager()
    cmd.join()
    print("Closing SecureDrop...")
    cleanup()
    