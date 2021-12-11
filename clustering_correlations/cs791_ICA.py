#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""

import mne
import os
from mne.preprocessing import ICA

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

filePath = "/Volumes/JorjaEEG/cs791_ica/"

#find files, make their path, and add to the list
for directory in dirsToCheck:
    dirFiles = os.listdir(directory)
    for file in dirFiles:
        if ".mff" in file:
            print(file)
            sessionData.append(os.path.join(directory,file))
            filename.append(file)

count = 0
total = 84 #total number of files
#load in the data
for subject in filename:
    file = sessionData[count]
    count += 1 #keep track of the number of participants, indexing starts @ 0
    raw = mne.io.read_raw_egi(file, preload = "True")
    filtRaw = raw.copy().filter(l_freq=0.05, h_freq=60)

    #calc the ica
    ica = ICA(n_components = 146, max_iter = 'auto', random_state = 27)
    ica.fit(filtRaw)
    outputName = filePath + subject[:-4] + "-ica.fif"
    
    ica.save(fname = outputName)
    
    print("Done with", count, "out of", total, "and ", total-count, "left.")
    print("[][][][][][][][][][][][][][][][][][][][]")



