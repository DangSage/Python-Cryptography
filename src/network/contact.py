from .tcp import tcp_client
import json
import nglobals as ng
import globals as gl
from utility import yes_no_prompt, list_data, verify_contact
from .ndata import list_users, list_non_contacts, verify_user, verify_contact_req, display_list


def request_contact():
    contactee_email = input("Enter Email (q to quit): ")
    # if contactee_email is an exit command
    for cmd in gl.EXIT_CMD:
        if contactee_email == cmd:
            return False
    if not verify_user(contactee_email):
        print("User not online. Please try again.")
    elif verify_contact_req(contactee_email) or verify_contact(contactee_email):
        print("Contact already added. Please try again.")
    try:
        tcp_client(verify_user(contactee_email), list_data(), "request")
    except Exception as e:
        print("Error: Could not send contact request: ", e)


def accept_contact():
    contacter_email = input("Enter Email (q to quit): ")
    for cmd in gl.EXIT_CMD:
        if contacter_email == cmd:
            return False
    if not verify_contact_req(contacter_email):
        return False
    try:
        tcp_client(verify_user(contacter_email), list_data(), "accept")
    except Exception as e:
        print("Error: Could not accept contact request: ", e)


def handle_contact():
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