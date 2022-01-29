# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 22:59:44 2022

@author: ranusingh1993
"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from Security import authenticate, identity

from User import UserRegister

app = Flask(__name__)
api = Api(app)

app.secret_key = 'ranu'

jwt = JWT(app,authenticate,identity)
app.config['PROPAGATE_EXCEPTIONS'] = True
items = []

'''next : it returns the next value in the iterator
   filter: filter function serach for values inside he iterator list according to function
   '''

class Item(Resource):
    '''For using them we need to add them as Item.parser.parse_args'''
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    
    
    @jwt_required()
    def get(self,name):
        '''item = variable   
           next = will return the next value in iteratore
           filter = 
        '''
        item = next(filter(lambda x:x['name']==name,items),None)
        return item,200 if item else 404
    
    @jwt_required()
    def post(self,name):
        if next(filter(lambda x:x['name']==name, items),None) is not None:
            return {'message':"An item with name'{}' already exists.".format(name)},400
        
        data = Item.parser.parse_args()
        item = {'name' :name,'price':data['price']}
        items.append(item)
        return item,201
    
    @jwt_required()
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message':'Item deleted'}
    
    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name,items),None)
        
        if item is None:
            item = {'name':name,'price':data['price']}
            items.append(item)
        
        else:
            item.update(data)
        
        return item
        
                                  
    
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'item':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run()