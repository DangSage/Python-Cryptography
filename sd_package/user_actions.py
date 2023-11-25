"""Module that contains functions that handle user actions such as registration, login, sending and accepting friend requests.
   It also contains functions for verifying users and getting user input."""

import getpass
from .cryptfuncs import generate_key_pair, encrypt_password, decrypt_password
from .user_data import load_user_data, save_user_data

def verify_user(email, password):
    user_data = load_user_data()
    if email in user_data:
        private_key = user_data[email]['private_key'].encode()
        stored_password = user_data[email]['password']
        decrypted_password = decrypt_password(private_key, stored_password)
        return decrypted_password == password
    return False

def send_friend_request(sender_email, receiver_email):
    user_data = load_user_data()
    if sender_email in user_data and receiver_email in user_data:
        if receiver_email not in user_data[sender_email]['friend_requests']:
            user_data[receiver_email]['friend_requests'].append(sender_email)
            save_user_data(user_data)
            print("Friend request sent!\n")
    else:
        print("Invalid sender or receiver email.\n")

def accept_friend_request(email, sender_email):
    user_data = load_user_data()
    if email in user_data and sender_email in user_data:
        if sender_email in user_data[email]['friend_requests']:
            user_data[email]['friends'].append(sender_email)
            user_data[sender_email]['friends'].append(email)
            user_data[email]['friend_requests'].remove(sender_email)
            save_user_data(user_data)
            print("Friend request accepted!\n")
        else:
            print("No friend request from this user.\n")
    else:
        print("Invalid email.\n")

def register_user():
    name = input("Enter Full Name: ")
    email = input("Enter an email: ")

    while True:
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.\n")


    private_key, public_key = generate_key_pair()
    encrypted_password = encrypt_password(public_key, password)

    user_data = load_user_data()
    user_data[email] = {
        'private_key': private_key.decode(),
        'full name': name,
        'password': encrypted_password,
        'friends': [],
        'friend_requests': []  
    }

    save_user_data(user_data)
    print("Registration successful!\n")

def get_user_input():
    email = input("Enter an email: ")
    password = getpass.getpass("Enter password: ")
    return email, password

def handle_friend_request(email, user_data):
    add_friend_choice = input("Do you want to send a friend request or accept one? (send/accept/logout): ")
    if add_friend_choice.lower() == 'send':
        receiver_email = input("Enter the email of the friend you want to send a request to: ")
        send_friend_request(email, receiver_email)
    elif add_friend_choice.lower() == 'accept':
        sender_email = input("Enter the email of the friend whose request you want to accept: ")
        accept_friend_request(email, sender_email)
    else:
        print("Logging out...")

