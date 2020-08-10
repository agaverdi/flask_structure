from app.models.model import User
from werkzeug.security import check_password_hash , generate_password_hash

def check_existence(email):
    
   
    
    if User.query.filter_by(email=email).first():
        return False
    else: 
        return True
     
def check_user(user_id):

    return True if User.query.filter_by(id=user_id).first() else False 

def password_hash(password):
    
    hash_password=generate_password_hash(password,"sha256")
    
    return hash_password

def check_password(hash_password, password):
    check=check_password_hash(pwhash=hash_password, password=password)

    if check:
        return True
    
    return False
