'''This file is used to test the functionality of the milestone 1-3 code.

At this point, users can register, login, and send friend requests to other users.
The database is stored in a JSON file, and passwords are encrypted using RSA encryption.

These first milestones do not implement any sort of secure messaging, or network functionality.'''

# To run, use the command: python -m test.milestone_1-3

import os
from ..sd_package import (
    load_user_data, 
    verify_user, 
    register_user, 
    get_user_input, 
    handle_friend_request
)

def display_user_info(email, user_data):
    user_friends = user_data[email].get('friends', [])
    print("Your friends: ", user_friends)
    print("Friend Requests: ", user_data[email]['friend_requests'])

def login_user():
    email, password = get_user_input()

    if verify_user(email, password):
        print("Login successful!\n")
        user_data = load_user_data()
        display_user_info(email, user_data)
        handle_friend_request(email, user_data)
    else:
        print("Login failed. Invalid username or password.\n")

def main():    
    while True:
        # Check if users.json exists in the current directory
        if not os.path.exists('users.json'):
            print("No users are registered with this client.")
            choice = input("Would you like to register a new user? (y/n): ")
            if choice.lower() == 'y':
                print()
                register_user()
                print()
                break
            else:
                break
        print("Welcome to the secure messaging client!\n")
        print("1. Register")
        print("2. Login")
        print("3. Quit\n")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            register_user()
            break
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Invalid selection. Please select 1, 2, or 3.\n")
    
    print("Exiting SecureDrop.")
    exit()

if __name__ == '__main__':
    main()