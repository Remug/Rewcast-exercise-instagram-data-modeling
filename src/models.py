import os
import sys
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    registration_date = Column(DateTime, default=datetime.now)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_text = (String(250))
    created_at = Column(DateTime, default=datetime.now)

    comments = relationship('Comments', backref='post')
    media = relationship('Media', backref='posts')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    posts_id = Column(Integer, ForeignKey('posts.id'))
    url = Column(String)

    posts = relationship('Posts', backref='media')

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    comment_text = (String(250))
    created_at = Column(DateTime, default=datetime.now)

    posts = relationship('Posts', backref='comments')
    author = relationship('Users')

class Follow(Base):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    following_id = Column(Integer, ForeignKey('users.id'))

    follower = relationship('Users', foreign_keys=[follower_id], backref='followers')
    following = relationship('Users', foreign_keys=[following_id])

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
