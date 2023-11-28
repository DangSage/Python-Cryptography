from utility import yes_no_prompt, load_user_data
from login import login_user
from registration import register_user
from sd_shell import start_cmd
from threading import Thread

def start():
    if load_user_data() != {}:
        print("Users are registered with this client.\n")
        inp = ""
        while inp != "1" and inp != "2" and inp != "q":
            print("(1) -> Login\n"
                  "(2) -> Register\n"
                  "(q) -> Quit\n")
            inp = input("Pick an option > ")
        inp = inp.lower()
        if inp == "1":
            login_user()
        elif inp == "2":
            register_user()
        elif inp == "q" or inp == "quit" or inp == "exit" or inp == "x":
            exit()
    else:
        print("No users are registered with this client.\n")
        yes_no_prompt("Do you want to register (y/n)? ", register_user, exit)

def run():
    start()
    print("\033[A\033[K\033[A\033[K")
    cmd = Thread(target=start_cmd)
    cmd.start()
    #TODO add thread to receive messages and new contacts from server
    cmd.join()
