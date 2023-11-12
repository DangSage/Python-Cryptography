# Milestone 1-3 Note: If user info not generating/populating in users.json, delete the users.json file, and then rerun the program

import json
import os
import getpass
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def encrypt_password(public_key, password):
    public_key = serialization.load_pem_public_key(public_key)
    encrypted_password = public_key.encrypt(
        password.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_password


def decrypt_password(private_key, encrypted_password):
    private_key = serialization.load_pem_private_key(private_key, password=None)
    decrypted_password = private_key.decrypt(
        encrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
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
        json.dump(user_data, file)


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
