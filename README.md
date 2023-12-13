# Secure Airdrop with Cryptography
This project aims to create a secure cryptographic version of an airdrop mechanism using Python. We will employ both symmetric and asymmetric cryptography, specifically RSA and AES, to achieve our goal.
  
  For external users, it's important to know the fundamental concepts of symmetric and asymmetric cryptography, as this project showcases their practical application in securing data transfers. Knowledge of Python and the PyCryptodome library will be helpful for understanding the implementation details.

Must have the pycryptodomex library installed to run using pip:
- ```pip install pycryptodomex```

SecureDrop also runs as a shell within the driver module ```secure_drop.py```. Run this driver module to start up the application.

## Milestones
The project is divided into milestones for each feature of the project. Current milestones are listed as below, with their features:

**Milestone 1 - User Registration**
  - Use simple file structures for data storage.
  - Implement security measures after initial testing.
  - Reuse password protections in User Login milestone.
  - Use Python crypt module for password security.
  - Generate and store data for future mutual using RSA encryption with SHA256 hashing.

**Milestone 2 - User Login**
  - Reuse code from User Registration milestone.
  - Use login data to enhance security in future milestones.
  - Clear all data from memory on program exit.

**Milestone 3 - Adding Contacts**
  - Use simple file structures for data storage.
  - Use Milestone 2 data to secure contact information.

**Milestone 4 - Detecting Contacts**
  - Use UDP connection to broadcast logins from other clients