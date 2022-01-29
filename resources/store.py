# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 19:53:11 2022

@author: ranusingh1993
"""

from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(),200
        return {"message":"Store ot found"},404
    
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"message":"Store already exists"},400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error occured while creating the store!"},500
        return store.json(),201
    
    
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()
            return {"message":"Store deleted"},200
        
        return {"message":"Store deleted sucessfully"},200
    
class StoreList(Resource):
    def get(self):
        return {'stores':[x.json() for x in StoreModel.find_all()]}
    
    
    