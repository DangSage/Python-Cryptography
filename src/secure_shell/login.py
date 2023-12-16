from utility import (
    load_user_data,
    get_email, 
    get_password,
    check_password
)
import globals as gl

def login_loop():
    attempts = 0
    user_data = load_user_data()
    email = get_email()

    if email in user_data:
        gl.USER_EMAIL = email
        gl.CONTACTS = list(user_data[email]['contacts'])
        gl.USER_NAME = user_data[email]['username']
        while attempts < gl.MAX_ENTRY_ATTEMPTS:
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
    
    if(attempts == gl.MAX_ENTRY_ATTEMPTS):
        print("\nMax password attempts reached!")
    print("\nExiting...")
    return False

def login_user():
    # login_loop() is called, if false program exits (failure)
    if not login_loop():
        exit()
