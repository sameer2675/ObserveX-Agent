import os
import sys
import json


if getattr(sys, "frozen", False):

    EXE_DIR = os.path.dirname(sys.executable)

    if os.path.basename(EXE_DIR).lower() == "main":
        BASE_DIR = os.path.dirname(EXE_DIR)
    else:
        BASE_DIR = EXE_DIR

else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

STORAGE_FILE = os.path.join(
    STORAGE_DIR,
    "registration_storage.json"
)


def save_registration_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_registration_data():
    if not os.path.exists(STORAGE_FILE):
        return None

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def already_registered():
    data = load_registration_data()

    if not data:
        return False

    return data.get("registered", False)