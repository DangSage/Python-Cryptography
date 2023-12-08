
import json
import re
import os
from getpass import getpass
from Cryptodome.PublicKey import RSA
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256

MIN_PASS_LENGTH = 8
MAX_ENTRY_ATTEMPTS = 3
USER_LIST = "users.json"
USER_EMAIL = ""
USER_NAME = ""
ONLINE_CONTACTS = []


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


def check_email():
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    email_attempts = 0

    while email_enter_attempts < MAX_ENTRY_ATTEMPTS:
        email = input("Enter email: ")
        if re.search(regex, email):
            print("Valid Email")
            email_enter_attempts = MAX_ENTRY_ATTEMPTS
            return email
        else:
            print("Invalid Email. Please try again.")
            email_attempts += 1


def save_user_data(user_data):
    with open(USER_LIST, 'w') as file:
        json.dump(user_data, file, indent=4)


def load_user_data():
    if os.path.exists(USER_LIST):
        with open(USER_LIST, 'r') as file:
            user_data = json.load(file)
            return user_data
    return {}


def hash_password(password):
    salt = os.urandom(16)
    password_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    return salt, password_hash


def check_password(salt, password_hash, password):
    # Hash the entered password in the same way as the stored password
    new_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    # Compare the new hash with the stored hash
    return new_hash == password_hash


def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem


def yes_no_prompt(prompt, yes_func, no_func=None):
    inp = ""
    while inp != "y" and inp != "n":
        inp = input(prompt)
        inp = inp.lower()
    if inp == "y":
        yes_func()
    elif inp == "n":
        if no_func is not None:
            no_func()

        
    


