# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:34:27 2022

@author: ranusingh1993
"""

import mysql.connector



connection = mysql.connector.connect(user='root',password='82497ee3',host ='localhost',database='data')
cursor = connection.cursor()
        
query = "SELECT * FROM users"
cursor.execute(query)
row = cursor.fetchone()
print(row)        