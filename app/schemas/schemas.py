from app.models.model import Cars , User , Post
from app.config.settings.extensions import  ma
from marshmallow import  validates_schema
from marshmallow import fields
from marshmallow.fields import  String, Email, UUID, Nested
from app.utils.helper import password_hash


class CarSchema(ma.SQLAlchemyAutoSchema):
    
    name = fields.String(required=True)

    class Meta:

        model         = Cars    
        load_instance = True 

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    name     = String(required=True)
    email    = Email(required=True)
    posts    = Nested("PostSchema", many=True)
    password = String(load_only=True,required=True)

    @validates_schema(skip_on_field_errors=True)
    def hashing_password(self, data, **kwargs):  
        print(data.get("password"))  
        print(data)
        
        hashed_pass = password_hash(data.get("password"))

        data.update(password=hashed_pass)

    class Meta:
        model         = User
        load_instance = True

class UserUpdateSchema(ma.Schema):
    name=String()
    email=Email()
    password=String(load_only=True)

    @validates_schema(skip_on_field_errors=True)
    def hashing_password(self, data, **kwargs):  
        if data.get("password"):
    
            hashed_pass = password_hash(data.get("password"))

            data.update(password=hashed_pass)


class PostSchema(ma.SQLAlchemyAutoSchema):
    title   = String(required=True)
    content = String(required=True)
    

    class Meta:
        model         = Post
        load_instance = True

