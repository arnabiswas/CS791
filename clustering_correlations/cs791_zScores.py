#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""

#Convert scores on different tasks to z-scores
import pandas as pd
import numpy as np
from scipy.stats import zscore

#Read in the csv files containing behavioral data for each task
task1 = pd.read_csv('task1.csv')
task2 = pd.read_csv('task2.csv')
task3 = pd.read_csv('task3.csv')
task4 = pd.read_csv('task4.csv')

#read in the IDs for the mTBI and control group
mtbi = pd.read_csv('mTBI_IDs.csv')
control = pd.read_csv('Control_IDs.csv')

#Make an empty list for keeping the participants being dropped:
#Reasons for droppping:
#No behavioral data 
#No eyes closed data
dropIndex = []
for subject in range(len(task1)):
    subID = task1['ID'][subject]
    
    #check to see if the IDs or in control or mTBI, otherwise drop
    if not(subID in list(mtbi['mTBI'])) and not(subID in list(control['ID'])):
        dropIndex.append(subject)
    elif subID == 4048:
        dropIndex.append(subject)
        
task1.drop(dropIndex, inplace = True)        
print("--------------")
print("Task 1 droppped", len(dropIndex), "participants.")

#Remove behavioral data 2 standard dev. away from the mean (outliers)
dMean, dStd = np.average(task1['Score']), np.std(task1['Score'])
lower, upper = dMean - (2*dStd), dMean + (2*dStd) 
prevN = len(task1)
task1 = task1[task1['Score'] > lower]
task1 = task1[task1['Score'] < upper]
print(prevN - len(task1), "outliers removed.")

#Do the same to all four tasks as task 1
dropIndex = []
for subject in range(len(task2)):
    subID = task2['ID'][subject]
    if not(subID in list(mtbi['mTBI'])) and not(subID in list(control['ID'])):
        dropIndex.append(subject)
    elif subID == 4048:
        dropIndex.append(subject)
        
task2.drop(dropIndex, inplace = True)   
print("--------------")
print("Task 2 droppped", len(dropIndex), "participants.")


dMean, dStd = np.average(task2['Score']), np.std(task2['Score'])
lower, upper = dMean - (2*dStd), dMean + (2*dStd) 
prevN = len(task1)
task2 = task2[task2['Score'] > lower]
task2 = task2[task2['Score'] < upper]
print(prevN - len(task1), "outliers removed.")

dropIndex = []
for subject in range(len(task3)):
    subID = task3['ID'][subject]
    if not(subID in list(mtbi['mTBI'])) and not(subID in list(control['ID'])):
        dropIndex.append(subject)
    elif subID == 4048:
        dropIndex.append(subject)
        
task3.drop(dropIndex, inplace = True)  
print("--------------")
print("Task 3 droppped", len(dropIndex), "participants.")
 

dMean, dStd = np.average(task3['Score']), np.std(task3['Score'])
lower, upper = dMean - (2*dStd), dMean + (2*dStd) 
prevN = len(task1)
task3 = task3[task3['Score'] > lower]
task3 = task3[task3['Score'] < upper]
print(prevN - len(task1), "outliers removed.")

dropIndex = []
for subject in range(len(task4)):
    subID = task4['ID'][subject]
    if not(subID in list(mtbi['mTBI'])) and not(subID in list(control['ID'])):
        dropIndex.append(subject)
    elif subID == 4048:
        dropIndex.append(subject)
        
task4.drop(dropIndex, inplace = True)  
print("--------------")
print("Task 4 droppped", len(dropIndex), "participants.")
 

dMean, dStd = np.average(task4['Score']), np.std(task4['Score'])
lower, upper = dMean - (2*dStd), dMean + (2*dStd)
prevN = len(task1) 
task4 = task4[task4['Score'] > lower]
task4 = task4[task4['Score'] < upper]
print(prevN - len(task1), "outliers removed.")

#zScore all the tasks
task1['Score'] = zscore(task1['Score'], nan_policy = 'omit')
task2['Score'] = zscore(task2['Score'], nan_policy = 'omit')
task3['Score'] = zscore(task3['Score'], nan_policy = 'omit')
task4['Score'] = zscore(task4['Score'], nan_policy = 'omit')

#Combine the zScores and save it to a file
scoreFile = pd.concat([task1, task2, task3, task4])
scoreFile = scoreFile.reset_index(drop = True)
scoreFile.to_csv('/Users/jorjashires/Documents/CS791_mTBI_Project/cs791_BehavioralData_ZScores.csv')

#Make a file for only mTBI zScores
mtbiOnly = []
for i in range(len(scoreFile)):
    subID = scoreFile['ID'][i]
    
    if subID in list(mtbi['mTBI']):
        subScore = scoreFile['Score'][i]
        mtbiOnly.append([subID, subScore])

mtbiOnly = pd.DataFrame(data = mtbiOnly, columns = ['ID', 'Score'])
mtbiOnly.to_csv('cs791_mtbiOnly_ZScores.csv')

#Make a file for only Control zScores
controlOnly = []
for i in range(len(scoreFile)):
    subID = scoreFile['ID'][i]
    
    if subID in list(control['ID']):
        subScore = scoreFile['Score'][i]
        controlOnly.append([subID, subScore])

controlOnly = pd.DataFrame(data = controlOnly, columns = ['ID', 'Score'])
controlOnly.to_csv('cs791_controlOnly_ZScores.csv')

