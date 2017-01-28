# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 13:01:24 2017

@author: mathi
"""

# -*- coding: utf-8 -*-

class Activity: #activity
    #constructor    
    def __init__(self, x, y,s=0.0):
        
        #position
        self.x_coord = x #x coordinate
        self.y_coord = y #y coordinate
        
        #score
        self.score = s

acti = Activity(0.0,0.0)

print acti.x_coord
print acti.y_coord

