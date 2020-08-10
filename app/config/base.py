import os 
import random

class Config:
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False