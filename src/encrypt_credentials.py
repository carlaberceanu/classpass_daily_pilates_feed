from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open(".secret", "wb") as key_file:
    key_file.write(key)

# Function to encrypt a message
def encrypt_message(message):
    with open(".secret", "rb") as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Credentials
username = input("Enter your username: ")
password = input("Enter your password: ")

# Encrypt and save the credentials
encrypted_username = encrypt_message(username)
encrypted_password = encrypt_message(password)

with open(".credentials", "wb") as file:
    file.write(encrypted_username + b"\n" + encrypted_password)

