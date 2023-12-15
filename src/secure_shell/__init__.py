'''The shell for the client. This is the main entry point for the client.'''

# Path: secure_shell/login.py

# Authors: Ethan, Matt, Spencer

# This file contains the login function for the client, and the functions that it uses.

from .login import (
    login_loop,
    login_user
)

from .registration import (
    valid_pass,
    register_user
)

from .sd_shell import (
    start_cmd
)