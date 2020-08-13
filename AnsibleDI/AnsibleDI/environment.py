import os
env = os.environ

DB = {
    "host": env.get("DB_HOST", "localhost"),
    "port": env.get("DB_PORT", "5432"),
    "name": env.get("DB_NAME", "ansb_inventory"),
    "username": env.get("DB_USER", "ansible"),
    "password": env.get("DB_PASS", "ansible_pass")
}

LOGGER = {
    "level": env.get("LOG_LEVEL", "INFO")
}