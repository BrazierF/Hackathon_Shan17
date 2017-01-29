#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 22:43:12 2017

@author: franckyinou
"""

import sql

def main(text,tMAx,nBest):
    activity_set = recuperer()
    tMax = 6
    nBest = 1
    resultat = journey_optimizer_master(activity_set, tMax, nBest)
    return resultat
