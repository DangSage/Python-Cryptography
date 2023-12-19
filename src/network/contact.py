from .tcp import tcp_client
import os
import json
import nglobals as ng
import globals as gl
from utility import yes_no_prompt, list_data, verify_contact, strip_file_path
from .ndata import (
    list_users, 
    list_online_contacts,
    list_non_contacts, 
    verify_user, 
    verify_contact_req, 
    display_list,
    user_name_of_email
)


def request_contact():
    contactee_email = input("Enter Email (q to quit): ")
    # if contactee_email is an exit command
    for cmd in gl.EXIT_CMD:
        if contactee_email == cmd:
            return False
    if not verify_user(contactee_email):
        print("User not online. Please try again.")
        return False
    elif verify_contact_req(contactee_email) or verify_contact(contactee_email):
        print("Contact already added. Please try again.")
        return False

    my_info = list_data()
    my_info = json.dumps(my_info)

    try:
        tcp_client(verify_user(contactee_email), my_info, "request")
    except Exception as e:
        print("Error: Could not send contact request: ", e)


def accept_contact():
    contacter_email = input("Enter Email (q to quit): ")
    for cmd in gl.EXIT_CMD:
        if contacter_email == cmd:
            return False
    if not verify_contact_req(contacter_email):
        return False
    
    my_info = list_data()
    my_info = json.dumps(my_info)

    try:
        tcp_client(verify_user(contacter_email), my_info, "accept")
    except Exception as e:
        print("Error: Could not accept contact request: ", e)


def handle_contact():
    '''
    Handle contact requests, both incoming and outgoing

    Incoming contact requests are displayed and the user is prompted to accept or reject them
    '''
    if ng.online_users == {}:
        list_users()
        return
    
    total_requests = len(ng.out_contact_requests) + len(ng.contact_requests)
    if total_requests > 0:
        display_list(
            "You have {} pending contact requests.".format(total_requests), 
            ng.out_contact_requests, 
            "Add some contacts!"
            )
    if len(ng.contact_requests) > 0:
        inp = ""
        inp = input("Do you want to accept a contact request (y/n)? ")

        if inp == "y" or inp == "yes":
            display_list("Contact requests:", ng.contact_requests, "HDWGH?")
            if accept_contact():
                return
        elif inp == "n" or inp == "no":
            return
    else:
        print("You have no incoming contact requests.")
        
    if list_non_contacts():
        yes_no_prompt("Do you want to send a contact request (y/n)? ", 
                    lambda: request_contact())
    return


def send_file():
    if not list_online_contacts():
        return False
    contactee_email = input("Enter Email (q to quit): ")
    # if contactee_email is an exit command
    for cmd in gl.EXIT_CMD:
        if contactee_email == cmd:
            return False
    if not verify_user(contactee_email):
        print("User not online. Please try again.")
        return False

    file_path = input("Enter file path: ")
    for cmd in gl.EXIT_CMD:
        if file_path == cmd:
            return False
    if not os.path.isfile(file_path):
        print("File does not exist!")
        return False

    file_name = file_path.split("/")[-1]
    try:
        # create dictionary of username and file path
        display_list("Sending:", {strip_file_path(file_name): user_name_of_email(contactee_email)}, "HDWGH?")
        yes_no_prompt(
            "Send file to contact? (y/n) >", 
            lambda: tcp_client(verify_user(contactee_email), file_path, file_name, True))
    except Exception as e:
        print("Error: Could not send file: ", e)
        