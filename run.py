from utility import yes_no_prompt, load_user_data
from login import login_user
from registration import register_user
from sd_shell import start_cmd
from threading import Thread

def start():
    if load_user_data() != {}:
        print("Users are registered with this client.\n")
        options = {
            "1": login_user,
            "2": register_user,
            "q": exit,
            "quit": exit,
            "exit": exit,
            "x": exit
        }
        inp = ""
        while inp not in options:
            print("(1) -> Login\n"
                  "(2) -> Register\n"
                  "(q) -> Quit\n")
            inp = input("Pick an option > ").lower()
        options[inp]()
    else:
        print("No users are registered with this client.\n")
        yes_no_prompt("Do you want to register (y/n)? ", register_user, exit)

def run():
    start()
    cmd = Thread(target=start_cmd)
    cmd.start()
    #TODO add thread to receive messages and new contacts from server
    cmd.join()
