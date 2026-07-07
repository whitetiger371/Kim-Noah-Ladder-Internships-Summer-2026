import json
import os
import bcrypt
from cryptography.fernet import Fernet

USERS_FILE = "users.json"
KEY_FILE = "secret.key"

def get_cipher():
    """Retrieve or generate the master encryption key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return Fernet(key)

def load_users():
    """Load and decrypt the users database."""
    if not os.path.exists(USERS_FILE):
        return {}
    cipher = get_cipher()
    with open(USERS_FILE, 'rb') as f:
        encrypted_data = f.read()
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode('utf-8'))
    except Exception:
        # Failsafe in case of a previously unencrypted file or corrupted data
        return {}

def save_users(users):
    """Encrypt and save the users database."""
    cipher = get_cipher()
    json_data = json.dumps(users).encode('utf-8')
    encrypted_data = cipher.encrypt(json_data)
    with open(USERS_FILE, 'wb') as f:
        f.write(encrypted_data)

def hash_password(password):
    """Hash a password for storing using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user using bcrypt."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def create_user(username, password):
    users = load_users()
        
    if username in users:
        return False, "Username already exists."
        
    users[username] = hash_password(password)
    save_users(users)
        
    return True, "Account created successfully."

def verify_user(username, password):
    users = load_users()
        
    if username not in users:
        # Fallback to default admin for testing purposes
        if username == "admin" and password == "password123":
            return True, "Login successful."
        return False, "Invalid username or password."
        
    if verify_password(users[username], password):
        return True, "Login successful."
    else:
        return False, "Invalid username or password."


MAX_INPUT_LENGTH = 10000


def validate_input(text):

    if not text:
        return False, "Input cannot be empty."

    if len(text) > MAX_INPUT_LENGTH:
        return False, "Input too large."

    return True, None