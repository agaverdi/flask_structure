from .base import  Config
from datetime import timedelta
import os

class Development(Config):

    SQLALCHEMY_DATABASE_URI = "postgres:///testdblast_2"

    # SQLALCHEMY_DATABASE_URI = "postgresql:///testdb"
    DEVELOPMENT = True
    ASSETS_DEBUG = True   
    DEBUG = True
    
    JWT_SECRET_KEY=os.urandom(32)                     #Bizim random sekret keyimiz
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=100)   #bitme vaxti
