import json
import globals as gl
import nglobals as ng
from utility import verify_contact

def display_list(msg1, data_dict, msg2):
    '''display list of data in top down list format
    i = index of item in list (for formatting)
    item = item in list (for formatting)'''

    print(msg1)
    if len(data_dict) == 0:
        print(f" └─{msg2}\n")
        return False
    else:
        for key, value in data_dict.items():
            #if last item in list
            if key == list(data_dict.keys())[-1]:
                print(" └─", end="")
            else:
                print(" ├─", end="")
            print(f"─{key}: {value}")
        print()
        return True


def list_users():
    return display_list("Online Users:", ng.online_users, "No users online.")


def list_non_contacts():
    non_contacts = {key: value for key, value in ng.online_users.items() if key not in ng.online_contacts}
    return display_list("Online Users:", non_contacts, "No users to contact.")


def list_online_contacts():
    '''list all online contacts in top down list format'''
    return display_list("Online Contacts:", ng.online_contacts, "No online contacts.")


def verify_user(email):
    '''
    verify if contact with email is online. 
    return the contact's TCP port if online.
    else return False
    '''
    for key, value in ng.online_users.items():
        if value[0] == email:
            return value[1]
    return False


def verify_contact_req(email):
    '''
    verify if contact with email is a pending contact request.
    (contact_requests, out_contact_requests)

    return True if contact is in contact_requests dictionary
    else return False
    '''
    for key, value in ng.contact_requests.items():
        if value[0] == email:
            return True
    for key, value in ng.out_contact_requests.items():
        if value[0] == email:
            return True
    return False


def parse_user_data(data, user_dict):
    '''
    data is a JSON string of the user's name, email, tcp_port, and bcast_port.
    data is converted to a list, and then added to the user_dict dictionary.
    
    returns the user's email if successful
    else returns False
    '''
    try:
        # convert data to list
        data = json.loads(data)
        
        key = data[0]
        values = [data[1], data[2], data[3]] # email, tcp_port, bcast_port
        user_dict.update({key: values})
        return key
    except IndexError:
        print("Client info invalid index {}".format(data))
        return False
    except json.decoder.JSONDecodeError:
        print("Client info invalid json encoding {}".format(data))
        return False

