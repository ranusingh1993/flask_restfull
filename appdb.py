# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:04:17 2022

@author: ranusingh1993
"""

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity
'''not required anymore with flask jwt extended library.'''
#from Security import authenticate, identity

from resources.User import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList

from resources.Itemdb import Item, ItemList

from datetime import timedelta
from db import db

from blacklist import Blacklist
app = Flask(__name__)
api = Api(app)

app.secret_key = 'ranu'
'''we don't need security.py file'''
jwt = JWTManager(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
username = 'root'
password = '82497ee3'
server = 'localhost'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/data".format(username, password, server)

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

app.config['JWT_BLACKLIST_ENABLED']= True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']   

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'description':'The token has expired.',
                    'error':'token_expired'}),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description':'Signature not verified',
                    'error':'Invalid_token'}),401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({'description':'Request needs fresh token to prcess'
                    ,'error':'requiired_fresh_token'}),401

@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify({'description':'Signature Required',
                    'error':'unauthorised request'}),401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'description':'token is no longer valid',
                    'error':'token has been revoked.'}),401
'''check blacklisted tokens'''
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    print(jti)
    return jti in Blacklist

'''use database or config file to load to add claims'''
@jwt.additional_claims_loader
def add_claim_to_jwt(identity):
    if identity == 2:
        return {'is_admin':True}
    return{'is_admin':False}

@app.before_first_request
def create_table():
    db.create_all()


if __name__ == "__main__":
    app.run()