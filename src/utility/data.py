
import json
import re
import os
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


def get_user_name_from_list():
    user_data = load_user_data()
    
    for user_email, user_info in user_data.items():
        if user_email == gl.USER_EMAIL:
            return user_info["username"]


def strip_file_path(file_path):
    '''strip file path from file name'''
    file_name = os.path.basename(file_path)
    return file_name


def display_list(msg1, data_dict, msg2, prefix=""):
    '''display list of data in branched-list format
    i = index of item in list (for formatting)
    item = item in list (for formatting)'''

    print(msg1)
    if len(data_dict) == 0:
        print(f"{prefix} └─{msg2}\n")
        return False
    else:
        for i, (key, value) in enumerate(data_dict.items()):
            if isinstance(value, dict):
                if i == len(data_dict) - 1:
                    print(f"{prefix} └─{key}:")
                elif i == 0:
                    print(f"{prefix} ├─{key}:")
                else:
                    display_list("", value, "No items.", prefix + " │ ")
            else:
                if i == len(data_dict) - 1:
                    print(f"{prefix} └─{key}: {value}")
                else:
                    print(f"{prefix} ├─{key}: {value}")
        print()
        return True


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

    gl.CONTACTS = user_data[gl.USER_EMAIL]["contacts"]
    for contact in gl.CONTACTS:
        if email == contact["email"]:
            return True
    for contact in ng.online_contacts:
        if email == contact["email"]:
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

