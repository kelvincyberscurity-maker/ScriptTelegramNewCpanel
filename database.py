import json
import os
from config import DEVELOPER_ID

DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"owners": [DEVELOPER_ID], "akses": []}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_owner(user_id):
    db = load_db()
    return user_id in db["owners"] or user_id == DEVELOPER_ID

def is_akses(user_id):
    db = load_db()
    return user_id in db["akses"] or is_owner(user_id)
