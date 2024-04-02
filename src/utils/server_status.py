import os
from src.utils.config import load_config

def server_status(setting_name):
    root_dir = os.path.abspath('.')
    if setting_name=="feishu":
        config = load_config(os.path.join(root_dir, 'config', 'config.yml'))["feishu"]
        if config['enable']:
            return True
        else:
            return False
    if setting_name=="mail":
        config = load_config(os.path.join(root_dir, 'config', 'config.yml'))["mail"]
        if config['enable']:
            return config
        else:
            return False