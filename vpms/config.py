import os
from dotenv import load_dotenv

load_dotenv()

class database:
    db_host = os.getenv("db_host")
    db_user = os.getenv("db_user")
    db_password = os.getenv("db_password")
    db_name = os.getenv("db_name")

class envelopment:
    DEBUG = os.getenv("envelopment") == 'dev'
    SECRET_KEY = os.getenv("secret_key")
