from utility import (
    load_user_data,
    MAX_ENTRY_ATTEMPTS,
    USER_NAME,
    USER_EMAIL,
    get_email, 
    get_password,
    check_password,
    PBKDF2,
    SHA256
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
            # get salt and stored password hash from user_data
            salt = bytes.fromhex(user_data[email]['password'].split(':')[0])
            stored_password_hash = bytes.fromhex(user_data[email]['password'].split(':')[1])
            if (check_password(salt, stored_password_hash, password)):
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
