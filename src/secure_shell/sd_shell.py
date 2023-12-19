
import globals as gl
from cmd import Cmd
import network as net
import nglobals as ng


class SecureDrop(Cmd):
    prompt = "secure_drop> "

    def do_add(self, inp):
        net.handle_contact()
    def help_add(self):
        print("   'add' -> Handle contact requests.")


    def do_users(self, inp):
        net.list_users()
    def help_users(self):
        print(" 'users' -> List all online users on the network.")


    def do_list(self, inp):
        net.list_online_contacts()
    def help_list(self):
        print("  'list' -> List all online contacts.")


    def do_send(self, inp):
        net.send_file()
    def help_send(self):
        print("  'send' -> Send a file to a contact.")


    def do_exit(self, inp):
        raise KeyboardInterrupt()
    def help_exit(self):
        print("  'exit' -> Exit SecureDrop. Shorthand: x q Ctrl-d")


    def do_me(self, inp):
        me = {}
        me[gl.USER_NAME] = {
            "Email": gl.USER_EMAIL, "Session Token": ng.session_token, 
            "Network" : {
                "IP": ng.own_ip, 
                "Ports": {"TCP": ng.tcp_port, "UDP": ng.bcast_port}}
        }
        net.display_list("Your Info:", me, "No contacts.")

    def help_me(self):
        print("    'me' -> Display my user info.")

    def do_help(self, inp):
        if inp > "":
            Cmd.do_help(self, inp)
        else:
            print("Available commands:")
            self.help_me()
            self.help_users()
            self.help_add()
            self.help_list()
            self.help_send()
            self.help_exit()
        if inp == "help":
            self.help_help()
    
    def help_help(self):
        print("  'help' -> List available commands with 'help' or detailed help with 'help cmd'.")


    def __init__(self):
        Cmd.__init__(self)
        self.intro = F"Welcome to SecureDrop {gl.USER_NAME}!\nType 'help' for a list of commands."

    def default(self, inp):
        if inp in gl.EXIT_CMD:
            return self.do_exit(inp)
        print("Unknown command: "+inp)

    do_EOF = do_exit
    help_EOF = help_exit


def start_cmd():
    try:
        ng.network_ready.wait()
        SecureDrop().cmdloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\nExiting...")
        ng.stop_threads.set()
        net.stop_tcp_listen()
        exit()