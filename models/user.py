# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:11:24 2022

@author: ranusingh1993
"""
import mysql.connector
from db import db
class UserModel(db.Model):
    
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self):
        return{"id" : self.id, 
               "username":self.username, 
               }
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_user_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
