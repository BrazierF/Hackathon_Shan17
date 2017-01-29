#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 22:43:12 2017

@author: franckyinou
"""

import sql,json,sys,time,os
texts = ['boire une biere','aller au parc','manger asiatique']

def main(text,tMax,nBest):
    activity_set = recuperer()
    with open("text_to_features/queries/q.txt", "w"):
        for st in texts:
            f.writelines(st+ "\n")
    scores=[0 for t in range(len(activity_set))]
    for i in range(len(texts)):
         with open("text_to_features/scores/out_"+str(i)+".txt", "r"):
            lines = f.readlines()
         for k,l in enumerate(lines) :
             scores[k]+= float(l[4:])
    for i in range (len(activity_set)):
        activity_set[i].score += scores[k]
    time.sleep(0.25)
    resultat = journey_optimizer_stochastic(activity_set, tMax, nBest) 
    
    printable  = '['
    #print resultat
    if len(resultat)>0:
        for x in resultat:
            printable  += '['
            #print x.toJSON()
            for y in x:
                printable += y.toJSON()+','
            printable = printable[:-1]
            printable  += '] ,'
        printable = printable[:-1]
    print printable+']'

if __name__ == "__main__":
    from sql import *
    from travel_generator import *
    import json,sys,time,os
    if len(sys.argv) > 1 : 
        #print sys.argv
        main(sys.argv[1],60*int(sys.argv[2]),int(sys.argv[3]))
    else:
        main('',6*60,1)
