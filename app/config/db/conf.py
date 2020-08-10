from app.config.settings.extensions import  db
import uuid
from sqlalchemy_utils import UUIDType
from datetime import datetime
import  os

Integer, String,BOOLEAN, DateTime, Column, ForeignKey,relationship, Text =  db.Integer, db.String,db.BOOLEAN, db.DateTime, db.Column,db.ForeignKey, db.relationship , db.Text

class Operation:

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        
        return self.save()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


class Model(Operation, db.Model):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id = Column(UUIDType(binary=False), primary_key=True,unique=True, default=uuid.uuid4)

    created_at = Column(DateTime, default=datetime.utcnow, server_default=db.func.now())

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,server_default=db.func.now())





