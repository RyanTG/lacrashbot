# -*- coding: utf-8 -*-
"""
Created on Tues Dec 22 17:08:42 2015

@author: herbie & ryan
"""
# STEP 1 of lacrashbot script package

# this module takes the whole tims data file, keeps only relevant fields,
# selects crashes in SCAG and bike crashes,
# and outputs csv files organized by year of crash

# set working directory
import os

# when on laptop
os.chdir('/home/rgratzer/Documents/Bot')

mydir = os.getcwd()

# import relevant modules using conventions in pandas documentation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# this get all data then delete blank rows approach has a long run time
# and produces a dtype / memory warning. it worked fine for the test files
# but needs some tweaking for the full file

# a chunker approach may bring down run time but i am not going to worry about this for now

#get data from csv
from pandas import read_csv
tims_csv = pd.read_csv('LosAngelesCounty2014/CollisionRecords.csv',
                       dtype = {'LOCATION':object, 'CHPTYPE': object, 'POP': object})
print "total rows in file"
print len(tims_csv.index)

# delete blank rows - the code below looks for CASE_ID values equal to NaN
# and keeps only rows that have a valid CASE_ID
tims = tims_csv[np.isfinite(tims_csv['CASE_ID'])]
print "total crashes in file"
print len(tims.index)

# only keep injury crashes
timsLAC = tims_csv[(tims_csv['COLLISION_SEVERITY'] > 0)]
print "Injury crashes in LAC: "
print len(timsLAC.index)
timsLAC.to_csv('LACinjury2014.csv')

