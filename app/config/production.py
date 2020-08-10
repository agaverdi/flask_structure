from .base import Config
import  os

class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    DEBUG = False
    SQLALCHEMY_ECHO = False

    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PASS = os.getenv("DB_PASS")
    DB_USER = os.getenv("DB_USER", "postgres")

    PRODUCTION = True