
import json
import re
import os
import base64
from getpass import getpass
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
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
    for email in user_data:
        user_data[email]['password'] = base64.b64encode(user_data[email]['password']).decode()

    with open(USER_LIST, 'w') as file:
        json.dump(user_data, file, indent=4)


def load_user_data():
    if os.path.exists(USER_LIST):
        email = None
        with open(USER_LIST, 'r') as file:
            user_data = json.load(file)
            for email in user_data:
                user_data[email]['password'] = base64.b64decode(user_data[email]['password'])
            if email == None:
                return {}
            else:
                return user_data
    return {}


def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem


def encrypt_password(public_key, password):
    public_key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    encrypted_password = cipher.encrypt(password.encode())

    return encrypted_password


def decrypt_password(private_key, encrypted_password):
    private_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    decrypted_password = cipher.decrypt(encrypted_password)

    return decrypted_password.decode()


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

        
    


