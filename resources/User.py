# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 18:57:56 2022

@author: ranusingh1993
"""
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel

from blacklist import Blacklist

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,help="username cannot be empty",type=str)
    parser.add_argument('password', required=True,help="password cannot be empty",type=str)
    
    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_user_by_username(data['username'])
        if user:
            return {"message":"Username already exists!"},400
        newUser = UserModel(data['username'],data['password'])
        newUser.save_to_db()
        
        return {"message":'User created sucessfully'}
        
class User(Resource):
    def get(self,user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message":"user not found"}
        return user.json()
    
    def delete(self,user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message":"user not found"}
        user.delete_from_db()
        return {"message":"user deleted sucessfully"}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,help="username cannot be empty",type=str)
    parser.add_argument('password', required=True,help="password cannot be empty",type=str)
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_user_by_username(data['username'])
        
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh = True)
            refresh_token = create_refresh_token(user.id)
            
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token
                }
        
        return{'Message':"Invalid credentials"},401
    
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token":access_token}
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        print(jti)
        Blacklist.add(jti)
        return {"message": "Successfully logged out"}