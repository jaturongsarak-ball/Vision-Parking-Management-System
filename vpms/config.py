import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

class Envelopment:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ENVELOPMENT = os.getenv("ENVELOPMENT")
    match ENVELOPMENT:
        case 'Development':
            DEBUG = True
        case 'Production':
            DEBUG = False
