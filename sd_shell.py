
from utility import *
import utility
from cmd import Cmd

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def request_contact(sender_email, receiver_email):
    user_data = load_user_data()
    if sender_email in user_data and receiver_email in user_data:
        if receiver_email not in user_data[sender_email]['contact_requests']:
            user_data[receiver_email]['contact_requests'].append(sender_email)
            save_user_data(user_data)
            print("Friend request sent!\n")
    else:
        print("Invalid sender or receiver email.\n")


def accept_contact(email, sender_email):
    user_data = load_user_data()

    if email in user_data and sender_email in user_data:
        if sender_email in user_data[email]['contact_requests']:
            user_data[email]['contacts'].append(sender_email)
            user_data[sender_email]['contacts'].append(email)
            user_data[email]['contact_requests'].remove(sender_email)
            save_user_data(user_data)
            print("Contact request accepted!\n")
            return True
        else:
            print("No contact request from this user.\n")
            return False
    else:
        print("Invalid email.\n")
        return False


def list_contacts():
    '''list all online contacts in top down list format'''
    print(GREEN + "Online Contacts:" + RESET)
    if len(ONLINE_CONTACTS) == 0:
        print("  No contacts online.")
    else:
        for contact in ONLINE_CONTACTS:
            print("  [{} ({})]".format(contact[0], (YELLOW + contact[1] + RESET)))

    print("\033[0m")


def handle_contact():
    user_data = load_user_data()
    email = utility.USER_EMAIL

    if len(user_data) == 1:
        print("No other users to contact.")
        return

    if len(user_data[email]['contact_requests']) > 0:
        print("You have {} pending contact requests.".format(len(user_data[email]['contact_requests'])))
        inp = ""
        while True:
            inp = input("Do you want to accept a contact request (y/n)? ")
            if inp == "y" or inp == "yes":
                print("Pending contact requests:")
                for i, contact in enumerate(user_data[email]['contact_requests']):
                    name = user_data[contact]['full name']
                    print("  {}) '{}' -> {}".format(i+1, name, contact))
                sender_email = input("\nEnter sender email: ")
                if accept_contact(email, sender_email):
                    break
            elif inp == "n" or inp == "no":
                break

    else:
        print("You have no pending contact requests.")
        yes_no_prompt("Do you want to send a contact request (y/n)? ", 
                      lambda: request_contact(email, input("Enter receiver email: ")))


class SecureDrop(Cmd):
    prompt = "secure_drop> "
    intro = "Welcome to SecureDrop.\nType 'help' to list commands\n"

    def do_add(self, inp):
        handle_contact()

    def help_add(self):
        print("  'add'  -> Handle contact requests.")


    def do_list(self, inp):
        list_contacts()

    def help_list(self):
        print("  'list' -> List all online contacts for current user.")


    def do_exit(self, inp):
        return True
    
    def help_exit(self):
        print("  'exit' -> Exit SecureDrop. Shorthand: x q Ctrl-d")


    def do_me(self, inp):
        print("   Email: "+utility.USER_EMAIL)
        print("   Alias: "+utility.USER_NAME+"\n")
    
    def help_me(self):
        print("  'me'   -> Display current user info.")


    def do_help(self, inp):
        SecureDrop.help_add(self)
        SecureDrop.help_list(self)
        SecureDrop.help_exit(self)
        SecureDrop.help_me(self)
        SecureDrop.help_help(self)

    def help_help(self):
        print("  'help' -> List available commands with 'help' or detailed help with 'help cmd'.")


    def default(self, inp):
        if inp == "x" or inp == "q":
            return self.do_exit(inp)
            print("Default {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit


def start_cmd():
    try:
        SecureDrop().cmdloop()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()