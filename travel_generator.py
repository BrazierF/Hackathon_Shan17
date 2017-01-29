
# coding: utf-8

# In[1]:

import numpy as np
import time as time


# In[2]

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


# In[3]:

class Journey:
    
    #constructor
    def __init__(self, idty=0, act=[]):
        self.idty=idty
        self.activities = act
        self.tour = range(len(act))
        self.tour_distance = 0.0
        self.score = 0.0
        self.nb_eval_dist=0
        
    def compute_score(self):
        return 0.0
    
    #remove one activity
    def remove(self, act):
        return
    
    #add one activity
    def insert(self, act):
        
        n=len(self.activities) #total number of activities currently in the journey
        
        if (n==0):
            self.tour.append(0)
            self.activities.append(act)
            return
        
        else:
        
            #activity act is inserted at the end of self.activities list
            #in the tour, we perform a least costly insertion
            
            #compute least costly insertion
            best_insertion = 1
            best_insertion_cost = np.inf
            for i in range(1,n+1):
                #compute improvement if (act) is inserted at position i
                insertion_cost = self.activities[self.tour[(i-1) %n]].distance(act) + self.activities[self.tour[i%n]].distance(act) - self.activities[self.tour[(i-1)%n]].distance(self.activities[(self.tour[i%n])]) 
                self.nb_eval_dist = self.nb_eval_dist+3
                
                if(insertion_cost < best_insertion_cost):
                    best_insertion = i
                    best_insertion_cost = insertion_cost
        
            #insert at best position
            self.tour.insert(best_insertion,n)
            #print 'Inserted', n, 'at position', best_insertion
            self.tour_distance = self.tour_distance+best_insertion_cost
            self.activities.append(act)
        
        return
    
    #replace activity1 by activity2
    def replace(self, act1, act2):
        
        self.remove(act1)
        self.insert(act2)
        n=len(self.activities)
        return
    
        #first, find act1's index and position in the tour
        act1_idx = 0
        act1_pos = 0
        for i in range(n):
            if self.activities[i]==act1:
                act1_idx = i
            if self.activities[tour[i]] ==act1:
                act1_pos = i
        
        print act1_idx, act1_pos
        
        #then, remove it from the tour
        tour_variation = - self.activities[self.tour[(act1_pos-1) %n]].distance(act1) - self.activities[self.tour[(act1_pos+1)%n]].distance(act1) + self.activities[self.tour[(act1_pos-1)%n]].distance(self.activities[(self.tour[(act1_pos+1)%n])]) 
        self.tour_distance = self.tour_distance + tour_improvement
        self.tour.remove(act1_pos)
        
        #replace act1 by act2 in the list of activities
        self.activities[act1_idx] = act2
        
        
        #compute least costly insertion
        best_insertion = 1
        best_insertion_cost = np.inf
        for i in range(1,n+1):
            #compute improvement if (act) is inserted at position i
            insertion_cost = self.activities[self.tour[(i-1) %n]].distance(act2) + self.activities[self.tour[i%n]].distance(act2) - self.activities[self.tour[(i-1)%n]].distance(self.activities[(self.tour[i%n])]) 
            self.nb_eval_dist = self.nb_eval_dist+3
              
            if(insertion_cost < best_insertion_cost):
                best_insertion = i
                best_insertion_cost = insertion_cost
        
        #insert at best position
        self.tour.insert(best_insertion,act1_idx)
        #print 'Inserted', n, 'at position', best_insertion
        self.tour_distance = self.tour_distance+best_insertion_cost
        return
        
    def two_opt(self):
        return


# In[ ]:

def journey_optimizer_master(activity_sets, tMax, nBest):
    
    #Activity_set[i] is a list of tuples (activity, score_acti, time_acti)
    #assume scores are weighted to reflect user's preferences for each type of activity
    
    #objective: find a subset of activities that maximise total score
    #while respecting some time constraint
    # => this is a knapsack problem
    
    nTypes = activity_sets.size() #number of activity types

    #1. merge all types of activities
    activities=[]
    for k in range(nTypes):
        for a in activity_sets[k]:
            activities.append(a)

    #2. sort activities by decreasing ratios score / time_needed 
    activities = sorted(activities, key=lambda x: x[1]/(x[2]+0.00001)) #protect from x[2] being 0.00
    
    #3. solve the knapsack problem
    #greedily add activities as long as the total duration is less than the max allowed
    t_tot=0.0
    nbActiSelected=0
    while(t_tot<=tMax):
        if (t_tot+activities[nbActiSelected][3] <= tMax):
            #add item
            nbActiSelected=nbActiSelected+1
            t_tot=t_tot+activities[nbActiSelected][3]
        else:
            break
    
    actiSelected = activities[range(nbActiSelected)]

    return actiSelected


# In[ ]:

def compute_tsp_tour(activities):
    
    n=len(activities)
    
    #construct distance matrix
    dist=np.zeros((n,n))
    
    for i in range(n):
        for j in range(i+1,n):
            #dist[i,j] = np.sqrt( np.square(activities[i].x_coord-activities[j].x_coord) + np.square(activities[i].y_coord-activities[j].y_coord))
            dist[i,j] = activities[i][0].distance[activities[j][0]]
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
    sorted_activities = [None]*n
    for i in range(i):
        sorted_activities=activities[tour_idx[i]]
        
    return sorted_activities