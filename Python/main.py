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
    for x in resultat:
        printable += x.toJSON()+','
    printable = printable[:-1]
    print printable+']'

if len(sys.argv) > 1 : 
    main(sys.argv[1],sys.argv[2],sys.argv[3])
else:
     main('',6,1)