#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jorjashires
"""

import mne
import os
import numpy as np
import matplotlib.pyplot as plt

#list of folders with data
dataFolder = '/Users/jorjashires/Documents/CS791_mTBI_Project/DATA'
dirsToCheck = []
for root, dirs, file in os.walk(dataFolder):
    for directory in dirs:
        print(directory)
        dirsToCheck.append(os.path.join(dataFolder, (directory + "/")))

#excluded follow-up folder, it has repeated data from session 5
#list to folder filenames
sessionData = {}
filename = []
subjectFound = []


#find files, make their path, and add to the list
for directory in dirsToCheck:
    dirFiles = os.listdir(directory)
    for file in dirFiles:
        if "Signals.Raw.edf" in file:
            print(file)
            oldName = os.path.join(directory,file)
            newName = file[:4] + "_" + file[5:9] + "_" + "Raw.edf"
            os.rename(oldName, os.path.join(directory, newName))
            if file[7] == '2':
                if not(file[:4] in sessionData):
                    sessionData[file[:4]] = []
                sessionData[file[:4]].append(os.path.join(directory, newName))
                filename.append(newName)
                if not(file[:4] in subjectFound):
                    subjectFound.append(file[:4])
        elif "_Raw.edf" in file:
            print(file)
            if file[7] == '2':
                if not(file[:4] in sessionData):
                    sessionData[file[:4]] = []
                sessionData[file[:4]].append(os.path.join(directory, file))
                filename.append(file)
                if not(file[:4] in subjectFound):
                    subjectFound.append(file[:4])


#Save files
filePathFilt = "/Volumes/JorjaEEG/cs791_filt_SP/"
filePathEpoch = "/Volumes/JorjaEEG/cs791_epoch_SP/"
filePathPDS = "/Volumes/JorjaEEG/cs791_power_SP/"
#Find all subjects that are useable
for subject in subjectFound:
    if subject == '4048':
        continue
    filesToLoad = sessionData[subject]
    raw = mne.io.read_raw_edf(filesToLoad[0], preload = True,
                              exclude = ['NA',
                                         'ESUTimestamp',
                                         'SystemTimestamp',
                                         'IRed',
                                         'Tilt X',
                                         'Tilt Y',
                                         'Tilt Z'])
    if len(filesToLoad) == 2:
        raw2 = mne.io.read_raw_edf(filesToLoad[1], preload = True,
                              exclude = ['NA',
                                         'ESUTimestamp',
                                         'SystemTimestamp',
                                         'IRed',
                                         'Tilt X',
                                         'Tilt Y',
                                         'Tilt Z'])
        raw.append([raw2])
    if len(filesToLoad) == 3:
        raw3 = mne.io.read_raw_edf(filesToLoad[2], preload = True,
                              exclude = ['NA',
                                         'ESUTimestamp',
                                         'SystemTimestamp',
                                         'IRed',
                                         'Tilt X',
                                         'Tilt Y',
                                         'Tilt Z'])
        raw.append([raw2, raw3])
    elif len(filesToLoad) == 4:
        raw3 = mne.io.read_raw_edf(filesToLoad[2], preload = True,
                              exclude = ['NA',
                                         'ESUTimestamp',
                                         'SystemTimestamp',
                                         'IRed',
                                         'Tilt X',
                                         'Tilt Y',
                                         'Tilt Z'])
        raw4 = mne.io.read_raw_edf(filesToLoad[3], preload = True,
                              exclude = ['NA',
                                         'ESUTimestamp',
                                         'SystemTimestamp',
                                         'IRed',
                                         'Tilt X',
                                         'Tilt Y',
                                         'Tilt Z'])
        raw.append([raw2, raw3, raw4])

        
    rawFilt = raw.copy().filter(l_freq = 0.05, h_freq = 60, picks = ['ECG', 'FzP0z', 'CzP0z'])
    rawEpoch = mne.make_fixed_length_epochs(rawFilt, duration = 120,
                                            preload = True,
                                            reject_by_annotation = False)
    
    tmin = 1
    tmax = 120
    fmin = 0.05
    fmax = 100
    sfreq = rawEpoch.info['sfreq']
    for channel in ['ECG', 'FzPOz', 'CzPOz']:
        psds, freqs = mne.time_frequency.psd_welch(
            rawEpoch,
            n_fft=int(sfreq * (tmax - tmin)),
            n_overlap=0, n_per_seg=None,
            tmin=tmin, tmax=tmax,
            fmin=fmin, fmax=fmax,
            verbose=False,
            picks = channel, 
            reject_by_annotation = False)
        
        outputName = filePathPDS + subject + "-" + channel + "-psds.npy"
        np.save(outputName, arr = psds)
        
        outputName = filePathPDS + subject + "-" + channel + "-freq.npy"
        np.save(outputName, arr = freqs)
    
    psds, freqs = mne.time_frequency.psd_welch(
        rawEpoch,
        n_fft=int(sfreq * (tmax - tmin)),
        n_overlap=0, n_per_seg=None,
        tmin=tmin, tmax=tmax,
        fmin=fmin, fmax=fmax,
        verbose=False,
        picks = ['ECG', 'FzPOz', 'CzPOz'], 
        reject_by_annotation = False)
    
    outputName = filePathPDS + subject + "-" + channel + "-psds.npy"
    np.save(outputName, arr = psds)
    
    outputName = filePathPDS + subject + "-" + channel + "-freq.npy"
    np.save(outputName, arr = freqs)
    
    #print("I'm here")
    
    #fig, axes = plt.subplots()
    #freq_range = range(np.where(np.floor(freqs) == 1.)[0][0],
    #               np.where(np.ceil(freqs) == fmax - 1)[0][0])

    #psds_plot = 10 * np.log10(psds)
    #psds_mean = psds_plot.mean(axis=(0, 1))[freq_range]
    #psds_std = psds_plot.std(axis=(0, 1))[freq_range]
    #axes.plot(freqs[freq_range], psds_mean, color='b')
    #axes.fill_between(freqs[freq_range], psds_mean - psds_std, 
    #                  psds_mean + psds_std, color='b', alpha=.2)
    #axes.set(title="PSD spectrum", ylabel='Power Spectral Density [dB]')
    #plt.show()
    
    #Save everything
    
    numpyData = rawFilt.get_data()
    np.save(filePathFilt + subject + "-filt.npy", arr = numpyData)
    
    numpyData = rawEpoch.get_data()
    np.save(filePathEpoch + subject + "-epoch.npy", arr = numpyData)
    
    outputName = filePathPDS + subject + "-psds.npy"
    np.save(outputName, arr = psds)
    
    outputName = filePathPDS + subject + "-freq.npy"
    np.save(outputName, arr = freqs)
