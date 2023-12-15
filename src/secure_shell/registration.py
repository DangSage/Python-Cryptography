from utility import (
    load_user_data,
    save_user_data,
    get_email,
    get_password,
    hash_password
)
import globals as gl
import binascii
from getpass import getpass

def valid_pass(password, confirm_password):
    '''return bool if password is valid, shouldn't be called outside of register_user()'''
    if password != confirm_password:
        print("Passwords don't match.")
        return False
    elif len(password) < gl.MIN_PASS_LENGTH:
        print("Password must be at least 8 characters long.")
        return False
    
    print("Password is valid! Registering User...")
    return True


def register_user():
    '''register user and save to user_data.json'''

    attempts = 0
    name = input("Enter Full Name: ")
    email = get_email()
    if email in load_user_data():
        print("\nUser with that email already registered!")
        exit()

    password = ""
    while True:
        password = get_password()
        confirm_password = getpass("Re-enter Password: ")
        if valid_pass(password, confirm_password):
            break
        attempts += 1
        if attempts >= gl.MAX_ENTRY_ATTEMPTS:
            print("Maximum password attempts reached.")
            return

    salt, hashed_password = hash_password(password)
    user_data = load_user_data()
    user_data[email] = {
        'username': name,
        'password': binascii.hexlify(salt).decode() + ":" + binascii.hexlify(hashed_password).decode(),
        'contacts': []
    }


    save_user_data(user_data)
    print("\nRegistration successful! Re-login...")
    exit()
