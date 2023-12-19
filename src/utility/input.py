from getpass import getpass
from globals import EXIT_CMD

def get_password():
    password = getpass("Enter password: ")
    return password


def get_email():
    email = input("Enter email: ")
    return email


def get_email_and_password():
    password = get_password()
    email = get_email()
    return (email, password)

def yes_no_prompt(prompt, yes_func, no_func=None):
    '''
    prompt user for yes or no input
    if yes, call yes_func
    if no, call no_func
    '''
    inp = ""
    while inp != "y" and inp != "n":
        inp = input(prompt)
        inp = inp.lower()
    if inp == "y":
        yes_func()
    elif inp == "n" or inp in EXIT_CMD:
        if no_func is not None:
            no_func()


