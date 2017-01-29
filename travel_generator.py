
# coding: utf-8

# In[1]:

import numpy as np
import time as time


# In[2]

class Activity: #activity
    #constructor    
    def __init__(self, name='',x=0.0, y=0.0,s=0.0,t=0.0):
        
        #name
        self.name = name
        #position
        self.x_coord = x #x coordinate
        self.y_coord = y #y coordinate
        
        #score
        self.score = s
        self.duration = t
        
    def distance(self,b):
        return np.sqrt( np.square(self.x_coord-b.x_coord) + np.square(self.y_coord-b.y_coord))
        #return ( np.square(self.x_coord-b.x_coord) + np.square(self.y_coord-b.y_coord))


# In[ ]:

def journey_optimizer_master(activity_set, tMax, nBest):
    
    #Activity_set is a list of activities
    #assume scores are weighted to reflect user's preferences for each type of activity
    
    #objective: find a subset of activities that maximise total score
    #while respecting some time constraint
    # => this is a knapsack problem
    
    #1. sort activities by decreasing ratios score / time_needed 
    activities = sorted(activity_set, key=lambda x: x.score / (x.duration+0.00001)) #protect from duration being 0.00
    
    #3. Approximately solve the knapsack problem
    #greedily add activities as long as the total duration is less than the max allowed
    t_tot=0.0
    nbActiSelected=0
    while(t_tot<=tMax):
        if (t_tot+activities[nbActiSelected].duration <= tMax):
            #add item
            nbActiSelected=nbActiSelected+1
            t_tot=t_tot+activities[nbActiSelected].duration
        else:
            break
    
    actiSelected = [activities[i] for i in range(nbActiSelected)]

    return actiSelected


# In[ ]:

def compute_tsp_tour(activities):
    
    n=len(activities)
    
    #construct distance matrix
    dist=np.zeros((n,n))
    
    for i in range(n):
        for j in range(i+1,n):
            #dist[i,j] = np.sqrt( np.square(activities[i].x_coord-activities[j].x_coord) + np.square(activities[i].y_coord-activities[j].y_coord))
            dist[i,j] = activities[i].distance(activities[j])
            dist[j,i] = dist[i,j]

   
    #start with greedy insertion
    tour_flag=[False]*n
    tour_idx=np.zeros(n)
    current_node=0
    for i in range(n):
        tour_idx[i]=current_node
        tour_flag[current_node]=True
        #find closest neighbour that is not in the tour
        closest_neighbour = current_node
        closest_distance = np.inf
        for j in range(n):
            if (tour_flag[j] or dist[current_node,j]>=closest_distance):
                #j is already in the tour
                continue
            else:
                closest_neighbour=j
                closest_distance = dist[current_node, j]
        
        current_node=closest_neighbour
    
    #compute tour
    sorted_activities=[None]*n
    for i in range(n):
        sorted_activities[i]=activities[int( tour_idx[i])]
        
    return sorted_activities