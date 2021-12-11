#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt 

#load electrode weights and channel locations
channelLocs = pd.read_csv('channelLocs.csv')
cheekLocs = pd.read_csv('cheekLocs.csv')
EGIweights = np.load('EGI_weights_1STD.npy')
prevWeights = np.load('1STDElectrodes.npy')
EGIweights = EGIweights[0:256] #each weight representing the electrodes

meanWeight = np.average(EGIweights)
stdWeight = np.std(EGIweights)

awayCrit = 2
upperLim = meanWeight + (stdWeight * awayCrit)
lowerLim = meanWeight - (stdWeight * awayCrit)

colorWeight = []
weightIndex = []
prevIndex = 0
for i in range(len(channelLocs)):
    if i in prevWeights:
        weight = EGIweights[prevIndex]
        prevIndex += 1
        if weight > upperLim:
            colorWeight.append(str(awayCrit) + "*std above mean")
            weightIndex.append(i)
        elif weight < lowerLim:
            colorWeight.append(str(awayCrit) + "*std below mean")
            weightIndex.append(i)
        else:
            colorWeight.append("Used in training")
    else:
        colorWeight.append("Within " + str(awayCrit) + "*std of mean")

sns.scatterplot(x = channelLocs['X1'], y = channelLocs['Y1'],
                hue = colorWeight, palette = {str(awayCrit) + "*std above mean": "red", 
                                              str(awayCrit) + "*std below mean": "blue", 
                                              "Within " + str(awayCrit) + "*std of mean": "black",
                                              "Used in training": "cyan"})

sns.despine(left = True, bottom = True)
plt.legend(loc = 'upper right')
plt.xticks([])
plt.yticks([])
plt.xlabel([], c = "w")
plt.ylabel([], c = "w")
plt.show()

np.save(str(awayCrit) + "STDElectrodesRR.npy", weightIndex)

# corX = []
# corY = []
# corEle = []
# upperX = 0.28
# upperY = 0.3
# lowerY = 0.1
# lowerX = -0.28
# for channel in range(len(channelLocs)):
#     chanX = channelLocs['X1'][channel]
#     chanY = channelLocs['Y1'][channel]
#     chanName = channelLocs['Elec'][channel]
#     if chanX > upperX and (chanY >= upperY or chanY >= lowerY):
#         continue
#     elif chanX < lowerX and (chanY >= upperY or chanY >= lowerY):
#         continue
#     elif chanY >= 0.45:
#         continue
#     elif chanName in [244, 234]:
#         continue
#     else:
#         corX.append(chanX)
#         corY.append(chanY)
#         corEle.append(channel)
        
# sns.scatterplot(x = corX, y = corY)