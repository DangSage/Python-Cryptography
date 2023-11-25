import os
from utility import USER_LIST
from login import login_user
from registration import register_user
from sd_shell import start_cmd
from threading import Thread

def start():
    if os.path.isfile(USER_LIST) and os.path.getsize(USER_LIST) > 0:
        # query for login or register
        inp = ""
        while inp != "l" and inp != "r":
            inp = input("Do you want to login or register (l/r)? ")
        if inp == "l":
            login_user()    
        elif inp == "r":
            register_user()
    else:
        print("No users are registered with this client.\n")
        inp = ""
        while inp != "y" and inp != "n":
            inp = input("Do you want to register a new user (y/n)? ")
        if inp == "y":
            register_user()
        elif inp == "n":
            exit(1)

def run():
    start()
    cmd = Thread(target=start_cmd)
    cmd.start()
    cmd.join()
