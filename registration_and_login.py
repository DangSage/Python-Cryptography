import json
import os
import getpass
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# Generate a unique key pair for each user
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

# Encrypt the password using the public key
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

# Decrypt the password using the private key
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

# Save user data to a JSON file


# Save user data to a JSON file
def save_user_data(user_data):
    # Encode the encrypted passwords as Base64 before saving to JSON
    for user in user_data:
        user_data[user]['password'] = base64.b64encode(user_data[user]['password']).decode()
    
    with open('users.json', 'w') as file:
        json.dump(user_data, file)

# Load user data from the JSON file
def load_user_data():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            try:
                user_data = json.load(file)
                # Decode the Base64-encoded passwords
                for user in user_data:
                    user_data[user]['password'] = base64.b64decode(user_data[user]['password'])
                return user_data
            except json.decoder.JSONDecodeError:
                return {}
    return {}

'''def save_user_data(user_data):
    with open('users.json', 'w') as file:
        json.dump(user_data, file)

# Load user data from the JSON file
def load_user_data():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}'''

# Register a new user
def register_user():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    private_key, public_key = generate_key_pair()
    encrypted_password = encrypt_password(public_key, password)

    user_data = load_user_data()
    user_data[username] = {
        'private_key': private_key.decode(),
        'password': encrypted_password
    }

    save_user_data(user_data)
    print("Registration successful!")

    '''username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    private_key, public_key = generate_key_pair()
    encrypted_password = encrypt_password(public_key, password)

    user_data = load_user_data()
    user_data[username] = {
        'private_key': private_key.decode(),
        'password': encrypted_password.decode()'''
    

    #save_user_data(user_data)
   # print("Registration successful!")

# Verify user credentials
def verify_user(username, password):
    user_data = load_user_data()
    if username in user_data:
        private_key = user_data[username]['private_key'].encode()
        stored_password = user_data[username]['password']#.encode()
        decrypted_password = decrypt_password(private_key, stored_password)
        return decrypted_password == password
    return False

# Login a user
def login_user():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if verify_user(username, password):
        print("Login successful!")
    else:
        print("Login failed. Invalid username or password.")

if __name__ == "__main__":
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
