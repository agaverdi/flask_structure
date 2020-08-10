from app.config.db.conf import Model, Integer, String,BOOLEAN, DateTime, Column, ForeignKey,relationship, UUIDType


class Cars(Model):

    __tablename__ = "cars"

    name = Column(String)


class User(Model):
    __tablename__ ="user"

    name  = Column(String)
    email = Column(String, unique=True)
    password=Column(String())
    posts = relationship("Post", backref="user")


class Post(Model):
    __tablename__="post"

    title   = Column(String)
    content = Column(String)

    user_id = Column(UUIDType(), ForeignKey("user.id"))