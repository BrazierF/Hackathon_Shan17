
# coding: utf-8

# In[1]:

import numpy as np
import json
import time as time
#import matplotlib.pyplot as plt

_columns = {
            'id':0,
            'type':1,
            'nom':2,
            'adresse':3,
            'lat':4,
            'lon':5,
            'duration':6,
            'score':7,
            'description':8,
            'tags':9,
            'vecteur':10,
            'extra':11}
            
_type = {
          'Parcs':0,
          'resto':1,
          'Evenements WE':2,
          'Patrimoine cult hist':3
          }
            

class Activity: #activity
    #constructor    
    def __init__(self, name='',type_='',lat=0.0, lng=0.0,s=0.0,t=0.0):
        
        #name
        self.name = name
        
        #GPS coordinates
        self.lat = float(lat) #latitude
        self.lng = float(lng) #longitude
        
        #score
        self.score = s
        self.duration = t
        
        self.type=type_
        
    def set_base_columns(self,row):
         #name
        self.name = row[_columns['nom']]
        
        #type
        self.type = row[_columns['type']]       
        
        #id
        self.id=row[_columns['id']]
        
        #address
        self.adresse=row[_columns['adresse']]
        
        #extra
        self.extra=row[_columns['extra']]
        
        #description
        self.description=row[_columns['description']]
 
        #duration
        self.duration = float(row[_columns['duration']])
        
        #tags
        self.tags = row[_columns['tags']]
        
        #score
        self.score = row[_columns['score']]
        
        #position
        self.lat =float(row[_columns['lat']]) #x coordinate
        self.lng = float(row[_columns['lon']]) #y coordinate
        
    def afficher(self):
         print self.name+' ('+str(self.lat)+','+str(self.lng)+')'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
            
    def distance(self,b):
        #return np.sqrt( np.square(self.x_coord-b.x_coord) + np.square(self.y_coord-b.y_coord)) #euclidean distance
        return 1.852 * 60.0 * np.arccos(np.sin(self.lat * np.pi / 180.)*np.sin(b.lat* np.pi / 180.)+np.cos(self.lat* np.pi / 180.)*np.cos(b.lat* np.pi / 180.)*np.cos((self.lng-b.lng)* np.pi / 180.)) #bird-fly distance, in km, using GPS coordinates
        #return ( np.square(self.x_coord-b.x_coord) + np.square(self.y_coord-b.y_coord))


# In[ ]:

def journey_optimizer_master(activity_set, tMax, nBest):
    
    #Activity_set is a list of activities
    #assume scores are weighted to reflect user's preferences for each type of activity
    n=len(activity_set)
    nType= 4 #only 4 different types ID in the DataBase as of now
    
    #objective: find a subset of activities that maximise total score
    #while respecting some time constraint
    # => this is a knapsack problem
    
    #1. sort activities by decreasing ratios score / time_needed 
    activities = sorted(activity_set, key=lambda x: -x.score / (x.duration+0.00001)) #protect from duration being 0.00
    
    #3. Approximately solve the knapsack problem
    #greedily add activities as long as the total duration is less than the max allowed
    t_tot=0.0
    nbActiSelected=0
    while(t_tot<=tMax and nbActiSelected<n):
        if (t_tot+activities[nbActiSelected].duration <= tMax):
            #add item
            t_tot=t_tot+activities[nbActiSelected].duration
            nbActiSelected=nbActiSelected+1
        else:
            break
    
    actiSelected = [activities[i] for i in range(nbActiSelected)]

    return compute_tsp_tour(actiSelected)

def journey_optimizer_stochastic(activity_set, tMax, nBest):
    
    nType=4
    #seperate activities by type (so we don't have three restaurants in a proposition)
    activitiesByType=[[]for i in range(nType)]
    scoreByType=[[]for i in range(nType)]
    softmaxByType=[[]for i in range(nType)]
    
    
    nbPerType=[0]*nType

    for a in activity_set:
#        print _type[a.type]
        activitiesByType[_type[a.type]].append(a)
        scoreByType[_type[a.type]].append(a.score)
        nbPerType[_type[a.type]] = nbPerType[_type[a.type]]+1
    
    #sort each activity set by decreasing score value
    for k in range(nType):
#        print '\tnbPerType', nbPerType[k], '; length of acti per Type', len(activitiesByType[k])
        activitiesByType[k] = sorted(activitiesByType[k], key=lambda x: -x.score)
        scoreByType[k] = sorted(scoreByType[k], key=lambda x: -x)
    
    #compute softmax values for scores
    for k in range(nType):
        #softmaxByType[k] = np.exp(scoreByType[k]) / np.sum(np.exp(scoreByType[k]))
        softmaxByType[k] = np.ones(nbPerType[k]) / (np.sum(np.ones(nbPerType[k]))+0.00001)
    
    #now generate random journeys, with at most one restaurant, one parcs, one buildings (if enough time) and one event 
    activities=[]

    start=time.time()
    
    iter=0
    while((time.time()-start<0.1) and (iter<10)):
        
        acti=[]
        
        #generate one activity per type, using the softmax values as the probability of choosing each element among a class
        sTot=0.0
        tTot=0.0
        for k in np.random.permutation(nType):
            r=np.random.rand()  #cast a random number
            #and decide which element of the set is added
            for i in range(nbPerType[k]):
                if(r<softmaxByType[k][i]):
                    acti.append(activitiesByType[k][i])
                    tTot=tTot+activitiesByType[k][i].duration
                    sTot=sTot+activitiesByType[k][i].score
#                    print 'iter',iter,'; type',k,'; act',i
                    break
                else:
                    r=r-softmaxByType[k][i]
                
            if tTot>tMax:
                #journey is too long : discard
                break
        
        if tTot>tMax:
            #journey is too long : discard
            break
        else:
            #journey respects the time constraint
            activities.append((acti,sTot))
        iter=iter+1
        
    #sort journeys by decreasing total score
    nbJourneys=len(activities)
#    print '\t\t', nbJourneys
#    print 'nbAppend=', nbAppend
    if nbJourneys==0:
        return []
    
    activities=sorted(activities, key=lambda x: -x[1])
    
    #only keep the nBest journeys, if they exist
    activities=[activities[i] for i in range(np.min([nbJourneys, 2*nBest]))]
    
    #finally, sort the remaining journeys, by computing their TSP tour approximations
    activities_sorted=[]

    for i in range(len(activities)):
        activities_sorted.append( (compute_tsp_tour(activities[i][0]),activities[i][1]))
    
    activities_sorted=sorted(activities_sorted, key=lambda x: -x[1]+x[0][1] / 1.0)
    
    activities=[]
    for i in range(len(activities_sorted)):
        print 'Score', activities_sorted[i][1],  'Dist', activities_sorted[i][0][1]
        activities.append(activities_sorted[i][0][0])
    
    
    
    return activities
    
    
# In[ ]:

def compute_tsp_tour(activities):
    
    n=len(activities)
    
    #construct distance matrix
    dist=np.zeros((n,n))
    
    for i in range(n):
        for j in range(i+1,n):
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
        
    total_dist=0.0
    for i in range(n):
        total_dist = total_dist+dist[int( tour_idx[i]), int( tour_idx[i]+1) % n]
    
    #print 'Total_Dist:', total_dist
    #compute tour
    sorted_activities=[None]*n
    for i in range(n):
        sorted_activities[i]=activities[int( tour_idx[i])]
        
    return (sorted_activities,total_dist)

np.random.seed(0)

acti_list=[]
start=time.time()
typeList=['Parcs',
          'resto',
          'Evenements WE',
          'Patrimoine cult hist']
for i in range(100):
    s=100*np.random.rand()
    w=2*np.random.rand()+0.25
    t=np.random.randint(0,4)
    a = Activity('',typeList[t],np.random.rand(),np.random.rand(),s,w)
    acti_list.append(a)


#acti_journey = journey_optimizer_master(acti_list, 6, 1)
#end=time.time()
#
#print end-start
#
#journey=acti_journey
#x=np.zeros(len(journey))
#y=np.zeros(len(journey))
#
#for i in range(len(journey)):
#    x[i]=journey[i].lat
#    y[i]=journey[i].lng
#    
#plt.plot(x,y,'o-')
#plt.show()

start=time.time()
acti_journey=journey_optimizer_stochastic(acti_list, 24, 10)
end=time.time()
print end-start

print len(acti_journey)

for journey in acti_journey:
    x=np.zeros(len(journey))
    y=np.zeros(len(journey))

    for i in range(len(journey)):
        x[i]=journey[i].lat
        y[i]=journey[i].lng
    
    plt.plot(x,y,'o-')
    plt.show()
