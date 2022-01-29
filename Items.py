# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 18:23:40 2022

@author: ranusingh1993
"""
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from Security import authenticate, identity


app = Flask(__name__)
api = Api(app)

app.secret_key = 'ranu'

jwt = JWT(app,authenticate,identity)
app.config['PROPAGATE_EXCEPTIONS'] = True
items = []

class Item(Resource):
    @jwt_required()
    def get(self,name):
        for item in items:
            if item['name'] == name:
                return item,200
            else:
                return {'item':None},404
    
    @jwt_required()
    def post(self,name):
        item = {'name':name,'price':12.00}
        items.append(item)
        return item,201
    
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'item':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



if __name__ == "__main__":
    app.run()