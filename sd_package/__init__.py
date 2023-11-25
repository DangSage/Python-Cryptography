# Authors: Ethan, Matt, Spencer
# Init file for the sd_package "SecureDrop" package.
#
# Importing the functions from the other files in the package within this folder.
# This allows us to use the functions in the other files without having to import each one individually.
# Pylance won't recognize these files as being used, but this is just a precompiled package, so it doesn't matter.

# Importing functions from encryption.py
# These functions are used for generating key pairs and encrypting and decrypting passwords
from .cryptfuncs import (
    generate_key_pair,
    encrypt_password,
    decrypt_password,
)

# Importing functions from user_data.py
# These functions are used for loading and saving user data
from .user_data import (
    load_user_data,
    save_user_data,
)

# Importing functions from user_actions.py
# These functions are used for user actions like verifying users, registering users, sending friend requests, etc.
from .user_actions import (
    verify_user,
    register_user,
    send_friend_request,
    accept_friend_request,
    get_user_input,
    handle_friend_request,
)