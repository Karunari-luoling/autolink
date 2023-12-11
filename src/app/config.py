import os
from flask import abort
from src.utils.config import load_config, update_config
from werkzeug.security import generate_password_hash

root_dir = os.path.abspath('.')
access_token = None
timer = None
BLACKLIST = set()

def block_token(token):
    BLACKLIST.add(token)

def get_password(password):
    password_config = load_config(os.path.join(root_dir, 'config', 'config.yml'))["basic_settings"]["password"]
    if password_config is not None:
        password_hash = generate_password_hash(password_config)
        return password_hash
    elif password_config is None:
        password_config = password
        update_config(os.path.join(root_dir, 'config', 'config.yml'),'basic_settings.password', password_config)
        password_hash = generate_password_hash(password)
        return password_hash
    else:
        abort(403)