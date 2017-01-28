# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 13:01:24 2017

@author: mathi
"""

import numpy as np
import matplotlib as plt

class Activity: #activity
    #constructor    
    def __init__(self, name='',x=0.0, y=0.0,s=0.0):
        
        #name
        self.name = name
        
        #position
        self.x_coord = x #x coordinate
        self.y_coord = y #y coordinate
        
        #score
        self.score = s
        
    def distance(self,b):
        return np.sqrt( np.square(self.x_coord-b.x_coord) + np.square(self.y_coord-b.y_coord))

def journey_optimizer(activity_sets, #list of tuples (activity set, n_type_min, n_type_max)
                      dur_min=0.0,
                      dur_max=np.inf, #max journey duration
                      dist_min=0.0,
                      dist_max=np.inf, #max travel distance
                      t_solve_max=1.0, #maximum time allowed for solving
                      ): 

    n = activities.size() #number of activity types
    n_tot = 1
    for k in range(n):
        n_tot = n_tot * len(activity_sets[k][0])

    
    
    
    
    
    
def tsp_distance(activities):
    
    n=len(activities)
    d=0.0
    
    #construct distance matrix
    dist=np.zeros((n,n))
    close_neighbours=np.zeros((n,n))
    
    for i in range(n):
        
        for j in range(i+1,n):
            #dist[i,j] = np.sqrt( np.square(activities[i].x_coord-activities[j].x_coord) + np.square(activities[i].y_coord-activities[j].y_coord))
            dist[i,j] = activities[i].distance[activities[j]]
            dist[j,i] = dist[i,j]
    for i in range(n):
        close_distance = np.inf #initialize closeest neighbours as being at distance of + Infty
        for j in range(n):
            if(i !=j ):
                if (dist[i,j] < close_distance):
                    close_neighbours[i]=j
                    close_distance = dist[i,j]
   
    #start with greedy insertion
    tour=np.zeros(n)
    visited = 
    for i in range(n):
        
    
    #apply 2-opt post-optimization
    
    
    return d
    
a=Activity('',0.0,0.0)
b=Activity('',1.0,1.0)

print tsp_distance([a,b])
    
