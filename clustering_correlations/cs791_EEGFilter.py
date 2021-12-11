#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""

import mne
import os
import numpy as np

#list of folders with data
dirsToCheck = ["/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_1/Chronic",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_1/Control",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_2",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_2/Control",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_3",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_4",
               "/Volumes/Hector_Dissertation/Hector_rs-EEG/Session_5"]
#excluded follow-up folder, it has repeated data from session 5
#list to folder filenames
sessionData = []
filename = []
#find files, make their path, and add to the list
for directory in dirsToCheck:
    dirFiles = os.listdir(directory)
    for file in dirFiles:
        if ".mff" in file:
            print(file)
            sessionData.append(os.path.join(directory,file))
            filename.append(file)


filePathNumpy = "/Volumes/JorjaEEG/cs791_filtered/numpy_Version/"
filePathFif = "/Volumes/JorjaEEG/cs791_filtered/fif_Version/"

count = 0
total = 84 #total number of files
for file in sessionData:
    if ".mff" in file:
        subFileName = filename[count]
        count += 1
        print("[][][][][][][][][][][][][][][][][][][]")
        print("Starting filtering of ", file)
        rawFile = mne.io.read_raw_egi(file, preload = "True") #read in EEG data
        rawFile_filtered = rawFile.copy().filter(l_freq = 0.05, h_freq = 60)
        outputFile = subFileName[:-4] #make the name for output file
        numpyData = rawFile_filtered.get_data() #get the data to save it
        np.save(filePathNumpy + outputFile + ".npy", arr = numpyData)
        rawFile_filtered.save(filePathFif + outputFile + ".fif", overwrite = True)
        print("Filtering complete.")
        print(count, " out of ", total, " done. ", total-count, "left.")


#Test filtering settings
#for lowCutoff in (50, 60):   
#    testFile_filtered = testFile.copy().filter(l_freq=0.05, h_freq=lowCutoff)
#    fig = testFile_filtered.plot(duration=60, proj = False, n_channels = 257, 
#                                remove_dc = True, group_by = "original")
#    fig.subplots_adjust(top=0.9)
#    fig.suptitle("High pass filtered at {} Hz".format(lowCutoff), 
#                 size = 'xx-large', weight = 'bold')
#    
#    print("----------------------------")

