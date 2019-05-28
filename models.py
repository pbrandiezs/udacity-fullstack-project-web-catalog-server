#!/usr/bin/env python3

# Program: models.py
# Author: Perry Brandiezs
# Date: May 1, 2019
# Last Updated: May 28, 2019

# This program sets up the database used by application.py


from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired)

Base = declarative_base()

# You will use this secret key to create and verify your tokens
secret_key = ''.join(
    random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    password_hash = Column(String)
    email = Column(String)
    picture = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format. """
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'picture': self.picture
            }


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String, index=True, unique=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format. """
        return {
            'id': self.id,
            'category_name': self.category_name
            }


class ItemCatalog(Base):
    __tablename__ = 'ItemCatalog'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('Category.id'))
    item_name = Column(String)
    item_description = Column(String)
    user_id = Column(Integer, ForeignKey('User.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'id': self.id,
            'category_id': self.category_id,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'user_id': self.user_id
            }


engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.create_all(engine)
