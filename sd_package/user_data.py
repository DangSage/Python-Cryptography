"""Module used for reading and writing data to users.json and other user-related functions"""

import json
import os
import base64

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