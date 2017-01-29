#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 22:43:12 2017

@author: franckyinou
"""

import sql,json,sys

def main(text,tMax,nBest):
    activity_set = recuperer()
    resultat = journey_optimizer_master(activity_set, tMax, nBest) 
    printable  = '['
    #print resultat
    if len(resultat)>0:
        for x in resultat:
            #print x.toJSON()
            printable += x.toJSON()+','
        printable = printable[:-1]
        print printable+']'

if __name__ == "__main__":
    from sql import *
    from travel_generator import *
    import json,sys
    if len(sys.argv) > 1 : 
        print sys.argv
        main(sys.argv[1],60*int(sys.argv[2]),int(sys.argv[3]))
    else:
        main('',6*60,1)