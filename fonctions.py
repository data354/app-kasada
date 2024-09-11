import json
import hashlib
import os
from datetime import datetime

# File path for user data and log file
USER_DATA_FILE = "users.json"
LOG_FILE = "log.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        users = json.load(file)
    if username in users and users[username] == hash_password(password):
        log_action(username, "Logged in")
        return True
    return False

def update_password(username, new_password):
    with open(USER_DATA_FILE, "r") as file:
        users = json.load(file)
    users[username] = hash_password(new_password)
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

def create_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        users = {}
    else:
        with open(USER_DATA_FILE, "r") as file:
            users = json.load(file)
    users[username] = hash_password(password)
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        users = json.load(file)
    return username in users

def log_action(username, action):
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now()} - {username} - {action}\n")
