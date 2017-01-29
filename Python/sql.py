# -*- coding:  iso-8859-1 -*-
"""
Created on Sat Jan 28 14:10:59 2017

@author: franck
"""
import mysql.connector, datetime,os,googlemaps
from travel_generator import *
import pickle
from datetime import datetime

#gmaps = googlemaps.Client(key='AIzaSyC_ETnxWmysf3X-ymcuLCUYwZVGgiCinWk')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#print geocode_result
#print geocode_result[0]['formatted_address']
# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="transit",
#                                     departure_time=now)



def recuperer():
    cnx = mysql.connector.connect(user='Hackathon', password='Python2.7',
                                  host='127.0.0.1',
                                  database='hackathon2017')
    cursor = cnx.cursor()
    query = ("(SELECT * FROM lieux "
             "WHERE type='Patrimoine cult hist' AND lat IS NOT NULL LIMIT 2) UNION  "
             "(SELECT * FROM lieux "
             "WHERE type='Evenements WE' AND lat IS NOT NULL LIMIT 2) UNION   "
             "(SELECT * FROM lieux "
             "WHERE type='resto' AND lat IS NOT NULL LIMIT 2) UNION   "
             "(SELECT * FROM lieux "
             "WHERE type='Parcs' AND lat IS NOT NULL LIMIT 2) ")
    
   # hire_start = datetime.date(1999, 1, 1)
    #hire_end = datetime.date(1999, 12, 31)
    
    cursor.execute(query)
    res=[]
    #row = dict(zip(cursor.column_names, cursor.fetchone()))
    row = cursor.fetchone()
    
    while row is not None:
        #print(row)
        #row = dict(zip(cursor.column_names, cursor.fetchone()))
        act = Activity(row[2],row[4],row[5])
        act.set_base_columns(row)
        res.append(act)
        #act.afficher()
        row = cursor.fetchone()
    #for item in cursor:
     #     print item
    #print cursor.fetchall()    
    cursor.close()
    cnx.close()
    return res

def parser(filename,cursor):    
    return


def ajouter_item(cursor,item):
    #print item
    if 'lat_v' not in item.keys() or  'lon_v' not in item.keys():
        add_item = ("INSERT INTO lieux "
                  "(type,nom,adresse,lat,lon,description,vecteur,extra) "
                  "VALUES (%(type_v)s, %(nom_v)s,%(adresse_v)s,DEFAULT,DEFAULT,%(description_v)s, %(vecteur_v)s, %(extra_v)s)")
    else:
         add_item = ("INSERT INTO lieux "
                  "(type,nom,adresse,lat,lon,description,vecteur,extra) "
                  "VALUES (%(type_v)s, %(nom_v)s,%(adresse_v)s,%(lat_v)s,%(lon_v)s,%(description_v)s, %(vecteur_v)s, %(extra_v)s)")
 
         
    # Insert salary information
    cursor.execute(add_item, item)
    
def const_item(type_lieu,tableau):
    for x in tableau :
        pass
        #print x
        
    if type_lieu == 'Parcs':
        item = {
          'type_v': type_lieu,
          'nom_v': tableau[0],
            'adresse_v':tableau[1],
              #'lat_v': 'DEFAULT' ,
          #'lon_v': 'DEFAULT',
            'description_v': tableau[-1],
            'vecteur_v': 'NULL',
            'extra_v': " ; ".join(x for x in tableau),
        }
        return trouver_adresse_gps(item)
        return item
    elif type_lieu == 'Patrimoine cult hist':
        item = {
          'type_v': type_lieu,
          'nom_v': tableau[0],
            'adresse_v':tableau[1],
              #'lat_v': 'DEFAULT' ,
          #'lon_v': 'DEFAULT',
            'description_v': tableau[-1],
            'vecteur_v': 'NULL',
            'extra_v': " ; ".join(x for x in tableau),
        }
        return trouver_adresse_gps(item)
        return item
    elif type_lieu == 'resto':
        item = {
          'type_v': type_lieu,
          'nom_v': tableau[0],
            'adresse_v':tableau[2],
              #'lat_v': 'DEFAULT' ,
          #'lon_v': 'DEFAULT',
            'description_v': tableau[1],
            'vecteur_v': 'NULL',
            'extra_v': " ; ".join(x for x in tableau),
        }
        return trouver_adresse_gps(item)
        return item       
    elif type_lieu == 'Evenements WE':
        item = {
          'type_v': type_lieu,
          'nom_v': tableau[1],
            'adresse_v':tableau[2],
              #'lat_v': 'DEFAULT' ,
          #'lon_v': 'DEFAULT',
            'description_v': tableau[-1],
            'vecteur_v': 'NULL',
            'extra_v': " ; ".join(x for x in tableau),
        }
        return trouver_adresse_gps(item)
    elif type_lieu == 'Toto':
        pass
        

def trouver_adresse_gps(item):
    adresse = item['adresse_v']
    if adresse.find('°') != -1:
        #print adresse
        coords = adresse.split(',')
        lat =  [int(s[:-1]) for s in coords[0].split()[:-1] if s[:-1].isdigit()]
        lat = lat[0] + lat[1]/60.0 + lat[2]/60.0/60.0
        lon =  [int(s[:-1]) for s in coords[1].split()[:-1] if s[:-1].isdigit()]
        lon = lon[0] + lon[1]/60.0 + lon[2]/60.0/60.0
        item['lat_v']=lat
        item['lon_v']=lon
        item['adresse_v']=''
    #print item
    if len(item['adresse_v']) == 0:
        if 'lat_v' and 'lon_v' in item.keys():
            result = gmaps.reverse_geocode((item['lat_v'], item['lon_v']))
            #print resultat[0]
            item['adresse_v']=result[0]['formatted_address']
            pass
        else:
            pass
    
    elif 'lat_v' not in item.keys() or  'lon_v' not in item.keys():
        res = gmaps.geocode(item['adresse_v'])
        item['lat_v']=res[0]['geometry']['location']['lat']
        item['lon_v']=res[0]['geometry']['location']['lng']
        item['adresse_v']=res[0]['formatted_address']
        pass
    
    return item

def ajouter(filename):
    if(not os.path.isfile(filename) ):
        return
    else:
        cnx = mysql.connector.connect(user='Hackathon', password='Python2.7',
                                      host='127.0.0.1',
                                      database='hackathon2017')
        type_lieu = filename.split('.csv')[0]
        cursor = cnx.cursor()
        k = open(filename, 'r')
        k.readline()
        for line in k.readlines():
            ajouter_item(cursor,const_item(type_lieu,line.split(';')))
        k.close()
        
        cursor.close()
            
        cursor = cnx.cursor()
        
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        
def recuperer():
    cnx = mysql.connector.connect(user='Hackathon', password='Python2.7',
                                  host='127.0.0.1',
                                  database='hackathon2017')
    cursor = cnx.cursor()
    query = ("(SELECT * FROM lieux "
             "WHERE type='Patrimoine cult hist' AND lat IS NOT NULL LIMIT 2) UNION  "
             "(SELECT * FROM lieux "
             "WHERE type='Evenements WE' AND lat IS NOT NULL LIMIT 2) UNION   "
             "(SELECT * FROM lieux "
             "WHERE type='resto' AND lat IS NOT NULL LIMIT 2) UNION   "
             "(SELECT * FROM lieux "
             "WHERE type='Parcs' AND lat IS NOT NULL LIMIT 2) ")
    
   # hire_start = datetime.date(1999, 1, 1)
    #hire_end = datetime.date(1999, 12, 31)
    
    cursor.execute(query)
    res=[]
    #row = dict(zip(cursor.column_names, cursor.fetchone()))
    row = cursor.fetchone()
    
    while row is not None:
        #print(row)
        #row = dict(zip(cursor.column_names, cursor.fetchone()))
        act = Activity(row[2],row[4],row[5])
        act.set_base_columns(row)
        res.append(act)
        #act.afficher()
        row = cursor.fetchone()
    #for item in cursor:
     #     print item
    #print cursor.fetchall()    
    cursor.close()
    cnx.close()
    return res

def recupererlo():
    cnx = mysql.connector.connect(user='Hackathon', password='Python2.7',
                                  host='127.0.0.1',
                                  database='hackathon2017')
    cursor = cnx.cursor()
    query = ("SELECT id,type,nom,tags,score FROM lieux ")
    
   # hire_start = datetime.date(1999, 1, 1)
    #hire_end = datetime.date(1999, 12, 31)
    
    cursor.execute(query)
    res=[]
    #row = dict(zip(cursor.column_names, cursor.fetchone()))
    row = cursor.fetchone()
    
    while row is not None:
        print(row)
        #row = dict(zip(cursor.column_names, cursor.fetchone()))
#        act = Activity(row[2],row[4],row[5])
#        act.set_base_columns(row)
        res.append(row)
#        act.afficher()
        row = cursor.fetchone()
    with open('toto.pkl','w') as f:
        pickle.dump(res,f)
    #for item in cursor:
     #     print item
    #print cursor.fetchall()    
    cursor.close()
    cnx.close()
    return res
recupererlo()
#ajouter('Patrimoine cult hist.csv')
#ajouter('Evenements WE.csv')
#ajouter('resto.csv')
#ajouter('Parcs.csv')
