#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 12:17:39 2021

@author: jorjashires
"""
import numpy as np
from matplotlib import pyplot as plt 
import pandas as pd
import os
import scipy.stats as stats
import seaborn as sns
from sklearn import preprocessing
from statsmodels.stats.multitest import multipletests
from matplotlib.patches import Ellipse


datasetLoc = ["/Volumes/JorjaEEG/cs791_psds_numpy/"]

behavioralResults = pd.read_csv('subjectDataClustering_Behavioral.csv')
egiConvertID = pd.read_csv('ID_To_Initials.csv')


spID = list(egiConvertID['ID'])
behavioralResults = behavioralResults[behavioralResults['ID'].isin(spID)]
subIDs = list(behavioralResults['ID'])
subIDs = egiConvertID[egiConvertID['ID'].isin(subIDs)]
subIDs = list(subIDs['Initials'])
subGroup = list(behavioralResults['GroupMem'])
subFiles = []

#Collect the order of the subjects
subInfo = []
test = []
for directory in datasetLoc:
    dirFiles = os.listdir(directory)
    for file in dirFiles:
        #SP
        #if ("-psds.npy" in file) and int(file[:4]) in subIDs:
            #subFiles.append(os.path.join(directory,file))
            
        
        
        #EGI
        if ("-psds.npy" in file) and file[:2] in subIDs and ("Session_1" in file) and ("-E" in file) and not(file[:3] in subIDs):
            subFiles.append(os.path.join(directory,file))
            
            #collect the subject info
            init = file[:2]
            spID = egiConvertID[egiConvertID['Initials'] == file[:2]]
            spID = int(spID['ID'])
            channel = file.split('-')
            channel = channel[1]
            group = behavioralResults[behavioralResults['ID'] == spID]
            group = int(group['GroupMem'])
            
            subInfo.append([spID, init, group, channel])
            test.append(group)

        elif ("-psds.npy" in file) and file[:3] in subIDs and ("Session_1" in file) and ("-E" in file):
            subFiles.append(os.path.join(directory,file))
            
            #collect the subject info
            init = file[:3]
            spID = egiConvertID[egiConvertID['Initials'] == init]
            spID = int(spID['ID'])
            channel = file.split('-')
            channel = channel[1]
            group = behavioralResults[behavioralResults['ID'] == spID]
            group = int(group['GroupMem'])
            
            subInfo.append([spID, init, group, channel])
            test.append(group)

            
        elif ("-psds.npy" in file) and file[:2] in subIDs and ("Control" in file) and not("Session" in file) and ("-E" in file) and not(file[:3] in subIDs):
            subFiles.append(os.path.join(directory,file))
            #collect the subject info
            init = file[:2]
            spID = egiConvertID[egiConvertID['Initials'] == file[:2]]
            spID = int(spID['ID'])
            channel = file.split('-')
            channel = channel[1]
            group = behavioralResults[behavioralResults['ID'] == spID]
            group = int(group['GroupMem'])
            
            subInfo.append([spID, init, group, channel])
            test.append(group)

        elif ("-psds.npy" in file) and file[:3] in subIDs and ("Control" in file) and not("Session" in file) and ("-E" in file):
            subFiles.append(os.path.join(directory,file))
            #collect the subject info
            init = file[:3]
            spID = egiConvertID[egiConvertID['Initials'] == file[:3]]
            spID = int(spID['ID'])
            channel = file.split('-')
            channel = channel[1]
            group = behavioralResults[behavioralResults['ID'] == spID]
            group = int(group['GroupMem'])
            
            subInfo.append([spID, init, group, channel])
            test.append(group)

lowAll = []
lowSub = []
highAll = []
highSub = []
conAll = []
conSub = []
for i in range(len(subFiles)):
    file = subFiles[i]
    subject = subInfo[i]
    
    dataFile = np.load(file)
    
    #dataAve = np.average(dataFile, axis = 1)
    dataAve = np.average(dataFile, axis = 0)
    dataAve = dataAve[0]
    
    if subject[2] == 0:
        highAll.append(dataAve)
        highSub.append(subject)
    elif subject[2] == 1:
        lowAll.append(dataAve)
        lowSub.append(subject)
    elif subject[2] == 2:
        conAll.append(dataAve)
        conSub.append(subject)
    
    
            

#make a list of all the channels, 1-256
channels = list(range(1, 257))
lowChan = []
highChan = []
conChan = []

#frequency ranges for the x-axis
freq = np.load('/Volumes/JorjaEEG/cs791_psds_numpy/BM_Session_1-E1-freq.npy')
sigChannels = []

badChan = pd.read_csv('offHeadLocs.csv')
badChan = list(badChan['Num'])

#alpha - 8 - 12
#1342:2057
#beta -  12 - 30
#2058:5279
#theta - 5 - 8
#805:1341
#gamma - >30
#5280:
#delta - 1 - 5
#89:804

#Normalize the data
lowAll = preprocessing.normalize(lowAll, axis = 1)
highAll = preprocessing.normalize(highAll, axis = 1)
conAll = preprocessing.normalize(conAll, axis = 1)

#put into log
lowAll = 10 * np.log10(lowAll)
highAll = 10 * np.log10(highAll)
conAll = 10 * np.log10(conAll)

#isolate the channel name for indexing later
lowChan = [item[3] for item in lowSub]
highChan = [item[3] for item in highSub]
conChan = [item[3] for item in conSub]

#Collect the stats, each band is a key
bandResults = {}
allResults = {}

#chanNum = []
#test each band, first two representing indexes of freq cutoffs
for band in [[1342, 2057, "Alpha"], [2058, 5279, "Beta"], [5280, 17811, "Gamma"], [805, 1341, "Theta"], [89, 804, "Delta"]]:
    lowPower = [item[band[0]:band[1]] for item in lowAll]
    highPower = [item[band[0]:band[1]] for item in highAll]
    conPower = [item[band[0]:band[1]] for item in conAll]
    
    statsLH = []
    statsCH = []
    statsCL = []
    
    sigChannels = []
    channelInfo = []
    chanNum = []
    for chan in channels:
        #isolate channels and average the frequency for the channels
        if chan in badChan:
            #skip channels not on the head
            continue
        
        chanNum.append(chan)
        
        channelName = "E" + str(chan)
        
        lowChanPower = []
        highChanPower = []
        conChanPower = []
    
        #gather the channel from each participant
        indexOfChannels = np.where(np.array(lowChan) == channelName)
        
        for i in indexOfChannels[0]:
            lowChanPower.append(lowPower[i])
            
        indexOfChannels = np.where(np.array(highChan) == channelName)
        
        for i in indexOfChannels[0]:
            highChanPower.append(highPower[i])
            
        indexOfChannels = np.where(np.array(conChan) == channelName)
        
        for i in indexOfChannels[0]:
            conChanPower.append(conPower[i])
        
        #find the average across
        lowChanPower = np.average(lowChanPower, axis = 1)
        highChanPower = np.average(highChanPower, axis = 1)
        conChanPower = np.average(conChanPower, axis = 1)
        
        #run a t-test
        lowHighF, lowHighp = stats.ttest_ind(lowChanPower, highChanPower, 
                                             equal_var = False)
        lowConF, lowConp = stats.ttest_ind(lowChanPower, conChanPower, 
                                             equal_var = False)
         
        highConF, highConp = stats.ttest_ind(highChanPower, conChanPower, 
                                             equal_var = False)
         
        statsLH.append(lowHighp)
        statsCH.append(highConp)
        statsCL.append(lowConp)
        
        #if (lowHighp < (0.05 / 80) or lowConp < (0.05 / 80) or highConp < (0.05 / 80)):
        #    sigChannels.append([channelName, lowHighp, lowConp, highConp, int(channelName[1:])])
        
        channelInfo.append([channelName, lowHighp, lowConp, highConp, int(channelName[1:])])
        
        bandResults[band[2] + channelName] = [np.average(lowChanPower), 
                                              np.average(highChanPower),
                                              np.average(conChanPower)]
    
    #Corretion for multiple comparisons
    #fdr_bh
    corLHp = multipletests(statsLH, method = "fdr_bh")
    corLCp = multipletests(statsCL, method = "fdr_bh")
    corHCp = multipletests(statsCH, method = "fdr_bh")
    
    corLHp = list(corLHp[1])
    corLCp = list(corLCp[1])
    corHCp = list(corHCp[1])
    
    
    for i in range(len(channelInfo)):
        channelInfo[i].append(corLHp[i])
        channelInfo[i].append(corLCp[i])
        channelInfo[i].append(corHCp[i])
        
    #save the stats results
    bandResults[band[2]] = sigChannels
    allResults[band[2]] = channelInfo
    
    
    
#used to plot entire frequency across band     

# for band in [[1342, 2057, "Alpha"], [2058, 5279, "Beta"], [5280, 17811, "Gamma"], [805, 1341, "Theta"], [89, 804, "Delta"]]:
#     lowPower = [item[band[0]:band[1]] for item in lowAll]
#     highPower = [item[band[0]:band[1]] for item in highAll]
#     conPower = [item[band[0]:band[1]] for item in conAll]
    
#     freqBand = freq[band[0]:band[1]]
    
#     for sigCh in bandResults[band[2]]:
#         lowY = []
#         highY = []
#         conY =[]
        
#         channelName = sigCh[0]
        
#         indexOfChannels = np.where(np.array(lowChan) == channelName)
        
#         for i in indexOfChannels[0]:
#             lowY.append(lowPower[i])
            
#         indexOfChannels = np.where(np.array(highChan) == channelName)
        
#         for i in indexOfChannels[0]:
#             highY.append(highPower[i])
            
#         indexOfChannels = np.where(np.array(conChan) == channelName)
        
#         for i in indexOfChannels[0]:
#             conY.append(conPower[i])
            
#         lowY = np.average(lowY, axis = 0)
#         highY = np.average(highY, axis = 0)
#         conY = np.average(conY, axis = 0)
            
#         sns.lineplot(x = freqBand, y = lowY, color = "orange")
#         sns.lineplot(x = freqBand, y = highY, color = "blue")
#         sns.lineplot(x = freqBand, y = conY, color = "green")
#         sns.despine()
#         plt.legend(["Low", "High", "Control"])
#         plt.ylim([-60, 0])
#         plt.ylabel("Spectral Power Density")
#         plt.xlabel("Frequency")
#         plt.title(channelName + ", " + band[2])
#         plt.show()
        
 
channelLocs = pd.read_csv('channelLocs.csv')
alphaP = 0.005 #alpha used, for corretions use 0.05, for now 0.005 for liberal use
indexLH = 1 #for corrections, + 4
indexLC = 2
indexHC = 3

#Find which bands are significant and plot them
for band in ["Alpha", "Theta", "Beta", "Gamma", "Delta"]:
    
    colorChan = []
    for chan in range(len(chanNum)):
        chanInfo = allResults[band][chan-1]
        
        if chanInfo[indexLH] < alphaP or chanInfo[indexLC] < alphaP or chanInfo[indexLC] < alphaP:
            colorChan.append("All")
            print(band)
            print(chan)
            print(chanInfo)
        elif chanInfo[indexLH] < alphaP and chanInfo[indexLC] < alphaP:
            colorChan.append("LowAll")
        elif chanInfo[indexLC] < alphaP and chanInfo[indexHC] < alphaP:
            colorChan.append("ControlAll")
        elif chanInfo[indexLH] < alphaP:
            colorChan.append("LowHigh")
            print(chanInfo[indexLH])
            print(chan)
        elif chanInfo[indexLC] < alphaP: 
            colorChan.append("LowControl")
            print(chanInfo[indexLC])
            print(chan)
        elif chanInfo[indexHC] < alphaP:
            colorChan.append("HighControl")
        else:
            colorChan.append("No")


    test = pd.read_csv('channelLocs.csv')
    plt.plot(dpi=300)
    ax = sns.scatterplot(x = test['X1'], y = test['Y1'], hue = colorChan,
                         palette=dict(All = "red",
                                      LowAll = "red",
                                      ControlAll = "cyan",
                                      LowHigh = "blue", 
                                      LowControl = "green",
                                      HighControl = "purple",
                                      No = "black"))
    ax.legend(loc = (0, -.1), mode = "expand", ncol = 6)
    sns.despine(top = True, bottom = True,
                right = True, left = True)
    ax.add_patch(Ellipse(xy = (0,0), width = (2 * 0.2413),
                             height = (2 * 0.313),
                             fill = None,
                             linewidth = 2))
    plt.xticks([])
    plt.yticks([])
    plt.xlabel([], c = "w")
    plt.xlim(-0.4, 0.4)
    plt.ylim(-0.4, 0.4)
    plt.ylabel([], c = "w")
    plt.title(band)
    plt.show()

#Pick a single electrode [#][3] to isolate for plotting and correlation
highlightElec = [[1342, 2057, "Alpha", 128], [2058, 5279, "Beta", 256], 
                  [805, 1341, "Theta", 141], [89, 804, "Delta", 53],
                  [5280, 17811, "Gamma", 17]]

#Create plot and correlate electrode for each band
for band in highlightElec:
    bandName = band[2]
    chanNum = band[3]
    channelName = "E" + str(chanNum)
    
    lowPower = [item[band[0]:band[1]] for item in lowAll]
    highPower = [item[band[0]:band[1]] for item in highAll]
    conPower = [item[band[0]:band[1]] for item in conAll]
    
    graphInfo = []
    
        
    indexOfChannels = np.where(np.array(lowChan) == channelName)
    #Gather all the data from the low mTBI
    for i in indexOfChannels[0]:
        
        ID = lowSub[i][0]
        group = 1
        groupLabel = 'Low'
        zScore = behavioralResults.loc[behavioralResults['ID'] == ID]
        zScore = float(zScore['Score'])
        
        bandAve = lowPower[i]
        bandAve = np.average(bandAve, axis = 0)
        
        graphInfo.append([ID, group, groupLabel, zScore, bandAve])
        
    indexOfChannels = np.where(np.array(highChan) == channelName)
    #Gather all data from high mTBI
    for i in indexOfChannels[0]:
        ID = highSub[i][0]
        group = 0
        groupLabel = 'High'
        zScore = behavioralResults.loc[behavioralResults['ID'] == ID]
        zScore = float(zScore['Score'])
        
        bandAve = highPower[i]
        bandAve = np.average(bandAve, axis = 0)
        
        graphInfo.append([ID, group, groupLabel, zScore, bandAve])
        
    indexOfChannels = np.where(np.array(conChan) == channelName)
    #Gather all data from control
    for i in indexOfChannels[0]:
        ID = conSub[i][0]
        group = 2
        groupLabel = 'Control'
        zScore = behavioralResults.loc[behavioralResults['ID'] == ID]
        zScore = float(zScore['Score'])
        
        bandAve = conPower[i]
        bandAve = np.average(bandAve, axis = 0)
        
        graphInfo.append([ID, group, groupLabel, zScore, bandAve])
    #Combine data into dataframe to make it easier to graph  
    graphInfo = pd.DataFrame(data = graphInfo, columns = ["ID", "GroupNum", 
                                                          "Group",
                                                          "z-Score", 
                                                        "Average SPD of Band"])
    ax = sns.scatterplot(x = graphInfo['Average SPD of Band'], 
                    y = graphInfo['z-Score'],
                    hue = graphInfo['Group'])
    #Scatter plot allows for group coloring...
    sns.regplot(x = graphInfo['Average SPD of Band'], 
                    y = graphInfo['z-Score'],
                    scatter = False)
    sns.despine()
    ax.legend(loc = (0.02, .8), ncol = 1)
    cor, p = stats.mstats.spearmanr(x = graphInfo['Average SPD of Band'], 
                    y = graphInfo['z-Score'])
    plt.title(bandName + ": " + channelName + " r = " + str(round(cor,2)) + " p = " + str(round(p,2)))
    plt.show() #graphs will overlap without this line due to loop
    
    
    
     
