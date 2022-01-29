# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:13:01 2022

@author: ranusingh1993
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 22:59:44 2022

@author: ranusingh1993
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


from models.item import ItemModel




'''next : it returns the next value in the iterator
   filter: filter function serach for values inside he iterator list according to function
   '''

class Item(Resource):
    '''For using them we need to add them as Item.parser.parse_args'''
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    parser.add_argument('store_id',type=int,required=True,help="This Store_id cannot be left blank")
    
    
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return{"message":"Item not found"}
        
        
    @jwt_required(fresh=True)
    def post(self,name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return {"message":"Item Already exists."},400
        
        data = Item.parser.parse_args()
        
        
        item = ItemModel(name,data['price'],data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return{"message":"An error occured while inserting the item"},500
        return item.json(),201
    
    
    @jwt_required()
    def delete(self,name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message':'Admin privillages are required.'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':"Item deleted"},200
        return{'message':"Item not found"}
    
    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        
        
        if item is None:
            try:
                item = ItemModel(name,data['price'],data['store_id'])
                
            except:
                return {"message":"An error occured while inserting item to database"}
        else:
            try:
                item.price = data['price']  
            except:
                return {"message":"An error occured while inserting item to database"}
        item.save_to_db()
        return item.json()
            
    
    
class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items":items},200
        return {'items':[item['name'] for item in items],
                "message":"More information available if you login."}
        
        



