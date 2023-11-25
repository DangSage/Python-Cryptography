from utility import (
    load_user_data,
    save_user_data,
    generate_key_pair,
    encrypt_password,
    get_email,
    get_password
)
from getpass import getpass

def register_user():
    name = input("Enter Full Name: ")
    email = get_email()
    password = get_password()

    confirm_password = getpass("Re-enter Password: ")
    
    while password != confirm_password:
        print("Passwords don't match.")
        password = get_password()
        confirm_password = getpass("Re-enter Password: ")

    private_key, public_key = generate_key_pair()
    encrypted_password = encrypt_password(public_key, password)

    user_data = load_user_data()
    user_data[email] = {
        'private_key': private_key.decode(),
        'full name': name,
        'password': encrypted_password,
        'contacts': [],
        'contact_requests': []  
    }

    save_user_data(user_data)
    print("\nRegistration successful! Re-login...")
    exit()
