# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 19:00:56 2022

@author: ranusingh1993
"""

from models.user import UserModel

# users = [User(1,'bob','bob')]

# username_mapping = {u.username:u for u in users}

# userid_mapping = {u.id:u for u in users}

def authenticate(username,password):
    user = UserModel.find_user_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_by_id(user_id)

