from utility import (
    load_user_data,
    save_user_data,
    generate_key_pair,
    encrypt_password,
    get_email,
    get_password,
    MIN_PASS_LENGTH,
    MAX_ENTRY_ATTEMPTS
)
from getpass import getpass

def valid_pass(password, confirm_password):
    '''return bool if password is valid, shouldn't be called outside of register_user()'''
    if password != confirm_password:
        print("Passwords don't match.")
        return False
    elif len(password) < MIN_PASS_LENGTH:
        print("Password must be at least 8 characters long.")
        return False
    
    print("Password is valid! Registering User...")
    return True


def register_user():
    '''register user and save to user_data.json'''

    attempts = 0
    name = input("Enter Full Name: ")
    email = get_email()
    if email in load_user_data():
        print("\nUser with that email already registered!")
        exit()

    password = ""
    while True:
        password = get_password()
        confirm_password = getpass("Re-enter Password: ")
        if valid_pass(password, confirm_password):
            break
        attempts += 1
        if attempts >= MAX_ENTRY_ATTEMPTS:
            print("Maximum password attempts reached.")
            return

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
