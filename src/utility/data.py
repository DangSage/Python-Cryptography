
import json
import re
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256

import globals as gl

def save_user_data(user_data):
    with open(gl.USER_LIST, 'w') as file:
        json.dump(user_data, file, indent=4)


def load_user_data():
    if os.path.exists(gl.USER_LIST):
        with open(gl.USER_LIST, 'r') as file:
            try:
                user_data = json.load(file)
            except json.decoder.JSONDecodeError:
                return {}
            return user_data
    return {}


def check_email():
    regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"
    email_attempts = 0

    while email_attempts < gl.MAX_ENTRY_ATTEMPTS:
        email = input("Enter email: ")
        if re.search(regex, email):
            print("Valid Email")
            email_attempts = gl.MAX_ENTRY_ATTEMPTS
            return email
        else:
            print("Invalid Email. Please try again.")
            email_attempts += 1


def hash_password(password):
    salt = os.urandom(16)
    password_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    return salt, password_hash


def check_password(salt, password_hash, password):
    new_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    return new_hash == password_hash


def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem


def get_user_name_from_list():
    user_data = load_user_data()

    username = user_data.get("full name")
    print(username)
    return username


def user_exists(user_dictionary, email):
    if user_dictionary[0].get("email") == email:
        return True
    return False


def check_contacts(data):
    user_data = load_user_data()

    user_email = list(user_data[0].keys())[0]
    email_exists = user_exists(user_data[0][user_email]["contacts"], data[1])
    return email_exists

        
def contacts_dict_exist():
    '''check if contacts dictionary exists in user_data.json'''
    with open(gl.USER_LIST, 'r') as file:
        data = json.load(file)

        user_email = list(data[0].keys())[0]

        u_dictionary = data[0][user_email]
        if "contacts" in u_dictionary:
            return True
    return False

    


