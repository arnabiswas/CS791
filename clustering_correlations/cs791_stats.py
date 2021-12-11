#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""
#import needed packagaes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats


#load files with data
dataFile = pd.read_csv('subjectDataClustering_Behavioral.csv')
dataFile = dataFile.dropna() #drop any na values

#make a box plot to see if data looks ok
ax = sns.boxplot(x = dataFile['GroupMem'], y = dataFile['Score'], data = dataFile) 
plt.show()



#empty lists to keep p values
ANOVA = []
conA = []
conB = []
conC = []
AB = []
AC = []
BC = []
controlZScores = []


#seperate the groups 
groupA = dataFile[dataFile['GroupMem'] == 0] #mTBI
groupB = dataFile[dataFile['GroupMem'] == 1] #mTBI
groupC = dataFile[dataFile['GroupMem'] == 2] #Control

#test if the groups violate normality 
#Answer: they do, use non-parametric
gANorm = stats.shapiro(groupA['Score'])
gBNorm = stats.shapiro(groupB['Score'])
gCNorm = stats.shapiro(groupC['Score'])

#Check if homoegentity is violated
Homo = stats.bartlett(groupA['Score'],
                        groupB['Score'],
                        groupC['Score'])

#It is, use kruskal
F, p = stats.kruskal(groupA['Score'],
                     groupB['Score'], 
                     groupC['Score'])

#Do the pairwise comparisons with kruskal
F_AB, p_AB = stats.kruskal(groupA['Score'],
                     groupB['Score'])
F_AC, p_AC = stats.kruskal(groupA['Score'],
                     groupC['Score'])

F_BC, p_BC = stats.kruskal(groupB['Score'],
                     groupC['Score'])

#Make a violin plot for paper
ax = sns.violinplot(x = dataFile["GroupMem"], y = dataFile["Score"])
sns.despine()
plt.plot(dpi=300) #make the graph high quality
plt.xticks(ticks = [0, 1, 2], 
                   labels = ['High', 'Low', 'Control'])
plt.ylabel("VWM z-Score")
plt.show()

