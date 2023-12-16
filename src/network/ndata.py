import json
import nglobals as ng
from utility import display_list


def list_users():
    return display_list("Online Users:", ng.online_users, "No users online.")


def list_non_contacts():
    non_contacts = {
        key: value for key, value in ng.online_users.items() if key not in ng.contact_requests and 
        key not in ng.out_contact_requests and key not in ng.online_contacts}
    return display_list("Online Users:", non_contacts, "No users to contact.")


def list_online_contacts():
    '''list all online contacts in top down list format'''
    return display_list("Online Contacts:", ng.online_contacts, "No online contacts.")


def user_name_of_connection(sock):
    '''return the username of the user connected to sock'''
    _, sock_port = sock.getpeername()
    for user, info in ng.online_users.items():
        print(f"{user}, {info[1]} vs {sock_port}")
        if info[1] == sock_port:
            return user
    raise ValueError("No user found with the given socket port number")


def user_name_of_email(email):
    '''return the username of the user with the given email'''
    for user, info in ng.online_users.items():
        if info[0] == email:
            return user
    raise ValueError("No user found with the given email")


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
    print("Contact request not found!")
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

