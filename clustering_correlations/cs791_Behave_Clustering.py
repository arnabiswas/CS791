#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""


import numpy as np
from matplotlib import pyplot as plt 
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import pandas as pd



def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
    
#read in z-score file 
dataFile = pd.read_csv('cs791_mtbiOnly_ZScores.csv')

scores = np.array(dataFile['Score'])
scores = scores.reshape(-1,1)

#cluster model, set no threshold so entire tree is generated
clusterModel = AgglomerativeClustering(distance_threshold = 0, n_clusters = None)

clusterModel = clusterModel.fit(scores)

plt.title("Clustering Results")
plot_dendrogram(clusterModel, truncate_mode = "level", p = 3)
plt.xlabel("Number of points in node")
plt.show()

#Decide where to cut by changing the number n_clusters is equal to
clusterModel = AgglomerativeClustering(n_clusters = 2, affinity= 'euclidean')
clusterModel = clusterModel.fit(scores)
labels = clusterModel.labels_

#Attach to the datafile
dataFile.insert(2, "GroupMem", labels, True)
#save
dataFile.to_csv('subjectDataClustering_Behavioral.csv')