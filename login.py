from utility import (
    load_user_data, 
    decrypt_password, 
    MAX_ENTRY_ATTEMPTS,
    USER_NAME,
    USER_EMAIL,
    get_email, 
    get_password
)
import utility

def login_loop():
    global USER_EMAIL
    global USER_NAME
    attempts = 0
    user_data = load_user_data()
    email = get_email()
    utility.USER_EMAIL = email

    if email in user_data:
        utility.USER_NAME = user_data[email]['full name']
        while attempts < MAX_ENTRY_ATTEMPTS:
            password = get_password()
            private_key = user_data[email]['private_key'].encode()
            stored_password = user_data[email]['password']
            decrypted_password = decrypt_password(private_key, stored_password)
            if decrypted_password == password:
                print("Login successful!")
                return True
            else:
                print("Incorrect password!")
                attempts += 1
    else:
        print("User with that email not registered!")
    
    if(attempts == MAX_ENTRY_ATTEMPTS):
        print("\nMax password attempts reached!")
    print("\nExiting...")
    return False

def login_user():
    # login_loop() is called, if false program exits (failure)
    if not login_loop():
        exit()
