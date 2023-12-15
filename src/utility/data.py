
import json
import re
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256

import globals as gl
import nglobals as ng

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
    
    for user_email, user_info in user_data.items():
        if user_email == gl.USER_EMAIL:
            return user_info["username"]


def list_data():
    '''
    returns a JSON object:
    [user_name, user_email, tcp_listen, bcast_port]
    '''
    data = [get_user_name_from_list(), gl.USER_EMAIL, ng.tcp_listen, ng.bcast_port]
    return json.dumps(data)


def add_contact(email, contact_data):
    '''add a contact to a user's contact list'''

    # load user data from file
    user_data = load_user_data()

    if email not in user_data:
        print("User not found!")
        return
    if contact_data[1] in user_data[email]['contacts']:
        print("Contact already exists!")
        return

    contact_entry = {
        "username": contact_data[0],
        "email": contact_data[1]
    }
    user_data[email]['contacts'].append(contact_entry)
    save_user_data(user_data)


def verify_contact(email):
    '''
    verify if contact with email is in any contacts dictionary.
    
    return True if contact is in contacts dictionary
    else return False
    '''
    user_data = load_user_data()

    for user_email, user_info in user_data.items():
        if user_email == gl.USER_EMAIL:
            if "contacts" in user_info:
                if email in user_info["contacts"]:
                    return True
    return False


def contacts_dict_exist():
    '''
    check if contacts dictionary exists in user_data.json for all users
    
    returns current user's contacts list if true
    else returns False
    '''
    with open(gl.USER_LIST, 'r') as file:
        data = json.load(file)

        for user_email, user_info in data.items():
            if "contacts" not in user_info:
                return False
        # return list of contacts
        return data[gl.USER_EMAIL]["contacts"]

    


