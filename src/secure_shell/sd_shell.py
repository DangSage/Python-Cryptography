
import globals as gl
from cmd import Cmd
import network as net
import nglobals as ng
from utility import display_list

class SecureDrop(Cmd):
    prompt = "secure_drop> "
    intro = "Welcome to SecureDrop.\nType 'help' to list commands\n"

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
        print("User: {}".format(gl.USER_NAME))
        print(" ├─Network")
        print(" |  ├─IP: {}".format(ng.own_ip))
        print(" |  └─Ports: ")
        print(" |      ├─TCP: {}".format(ng.tcp_port))
        print(" |      └─UDP: {}".format(ng.bcast_port))
        print(" └─Email: '{}'".format(gl.USER_EMAIL))
        print("")

    def help_me(self):
        print("    'me' -> Display current user info.")

    def do_help(self, inp):
        if inp > "":
            Cmd.do_help(self, inp)
        else:
            print("Available commands:")
            self.help_add()
            self.help_list()
            self.help_users()
            self.help_me()
            self.help_exit()
        if inp == "help":
            self.help_help()
    
    def help_help(self):
        print("  'help' -> List available commands with 'help' or detailed help with 'help cmd'.")


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
    except:
        print("\nExiting...")
        net.shutdown_event.set()
        net.stop_tcp_listen()
        exit()