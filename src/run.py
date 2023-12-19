from utility import yes_no_prompt, load_user_data, write_session_token
from secure_shell import (
    login_user,
    register_user,
    start_cmd
)
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


def run():
    start()
    cmd = Thread(target=start_cmd, daemon=True)
    cmd.start()
    network_manager()
    print("Closing SecureDrop...")
    