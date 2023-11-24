# Milestone 1-3 Note: If user info not generating/populating in users.json, delete the users.json file, and then rerun the program

import json
import os
import getpass
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256

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
    name = input("Enter a username: ")
    email = input("Enter an email: ")
    password = getpass.getpass("Enter password: ")

    private_key, public_key = generate_key_pair()
    encrypted_password = encrypt_password(public_key, password)

    user_data = load_user_data()
    user_data[email] = {
        'private_key': private_key.decode(),
        'username': name,
        'password': encrypted_password,
        'friends': [],
        'friend_requests': []  
    }

    save_user_data(user_data)
    print("Registration successful!\n")


def login_user():
    email = input("Enter an email: ")
    password = getpass.getpass("Enter password: ")

    if verify_user(email, password):
        print("Login successful!\n")
        user_data = load_user_data()
        user_friends = user_data[email].get('friends', [])
        print("Your friends: ", user_friends)
        print("Friend Requests: ", user_data[email]['friend_requests'])
        add_friend_choice = input("Do you want to send a friend request or accept one? (send/accept/logout): ")
        if add_friend_choice.lower() == 'send':
            receiver_email = input("Enter the email of the friend you want to send a request to: ")
            send_friend_request(email, receiver_email)
        elif add_friend_choice.lower() == 'accept':
            sender_email = input("Enter the email of the friend whose request you want to accept: ")
            accept_friend_request(email, sender_email)
        else:
            print("Logging out...")
            
    else:
        print("Login failed. Invalid username or password.\n")
    

def save_user_data(user_data):
    for email in user_data:
        user_data[email]['password'] = base64.b64encode(user_data[email]['password']).decode()

    with open('users.json', 'w') as file:
        json.dump(user_data, file, indent=4)


def load_user_data():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
                user_data = json.load(file)
                for email in user_data:
                    user_data[email]['password'] = base64.b64decode(user_data[email]['password'])
                return user_data
    return {}


def verify_user(email, password):
    user_data = load_user_data()
    if email in user_data:
        private_key = user_data[email]['private_key'].encode()
        stored_password = user_data[email]['password']
        decrypted_password = decrypt_password(private_key, stored_password)
        return decrypted_password == password
    return False


if __name__ == "__main__":
    while True:
        # Check if users.json exists in the current directory
        if not os.path.exists('users.json'):
            print("No users are registered with this client.")
            choice = input("Would you like to register a new user? (y/n): ")
            if choice.lower() == 'y':
                print()
                register_user()
            else:
                break
        print("Welcome to the secure messaging client!\n")
        print("1. Register")
        print("2. Login")
        print("3. Quit\n")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Invalid selection. Please select 1, 2, or 3.\n")
