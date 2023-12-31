
import json
import re
import os
import globals as gl
import nglobals as ng


def write_session_token():  # not in utility module
    '''
    write this clients session token to user_data.json
    '''
    user_data = load_user_data()
    user_data[gl.USER_EMAIL]["session_token"] = ng.session_token
    save_user_data(user_data)


def save_user_data(user_data):
    with open(gl.USER_LIST, 'w') as file:
        json.dump(user_data, file, indent=4)


def load_user_data():
    '''
    load user data from USER_LIST file
    '''
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


def get_user_name_from_list():
    user_data = load_user_data()
    
    for user_email, user_info in user_data.items():
        if user_email == gl.USER_EMAIL:
            return user_info["username"]


def strip_file_path(file_path):
    '''
    strip file path from file name
    '''
    file_name = os.path.basename(file_path)
    return file_name


def display_list(msg1, data_dict, msg2, prefix="", it=0):
    '''
    display list of data in tree format, using prefix to display tree structure

    all data is displayed as a dictionary, using box-drawing characters to display tree structure
    '''

    if it == 0:
        print(msg1)
    if len(data_dict) == 0:
        print(f"{prefix} └─{msg2}")
        return False
    else:
        for i, (key, value) in enumerate(data_dict.items()):
            if isinstance(value, dict):
                if i == len(data_dict) - 1: # if last item in dictionary
                    print(f"{prefix} └─{key}:")
                    new_prefix = prefix + "  "
                else:
                    print(f"{prefix} ├─{key}:")
                    new_prefix = prefix + " │"
                display_list("", value, "No items.", new_prefix + "  ", it+1)
            else:
                if i == len(data_dict) - 1:
                    print(f"{prefix} └─{key}: {value}")
                else:
                    print(f"{prefix} ├─{key}: {value}")
        return True


def list_data():
    '''
    returns a JSON object:
    [ username, user email, tcp port, udp port ]
    '''
    data = {'username': get_user_name_from_list(), 'email':gl.USER_EMAIL, 
            'tcp':ng.tcp_listen, 'udp':ng.bcast_port}
    return data


def add_contact(contact_data):
    '''
    add a contact to a user's contact list in USER_LIST file
    '''

    # load user data from file
    user_data = load_user_data()

    if contact_data['email'] in user_data[gl.USER_EMAIL]['contacts']:
        print("Contact already exists!")
        return

    contact_entry = {
        "username": contact_data['username'],
        "email": contact_data['email']
    }
    user_data[gl.USER_EMAIL]['contacts'].append(contact_entry)
    save_user_data(user_data)


def verify_contact(email):
    '''
    verify if contact with email is in any contacts dictionary.
    
    return True if contact is in contacts dictionary
    else return False
    '''
    user_data = load_user_data()

    gl.CONTACTS = user_data[gl.USER_EMAIL]["contacts"]
    for contact in gl.CONTACTS:
        if email == contact["email"]:
            return True
    for contact in ng.online_contacts:
        if email == contact["email"]:
            return True
        
    return False


def verify_session(email):
    '''
    verify if user has a session on this device
    '''
    user_data = load_user_data()
    if email in user_data:
        # if session token exists and is not equal to ng.SESSION_TOKEN return true
        if "session_token" in user_data[email] and user_data[email]["session_token"] != ng.session_token:
            return True
    return False


def verify_token(email, token):
    '''
    email = user's email pre-existing in ng.online_users
    token = session token given through a broadcast message.

    tokens are generated as get_random_bytes(12).hex()

    return True if token == token in ng.online_users for email
    return False if token != token in ng.online_users for email or token is not a valid token
    '''
     # Check if the token is a valid token
    if not re.match(r'^[a-f0-9]{24}$', token):
        return False

    # Check if the email exists in ng.online_users and if the token matches
    if email in ng.online_users and 'session_token' in ng.online_users[email]:
        return ng.online_users[email]['session_token'] == token

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

