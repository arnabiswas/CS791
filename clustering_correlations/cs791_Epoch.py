#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 10:00:17 2021

@author: jorjashires
"""

import mne
import os
import numpy as np

#list of folders with data
dirsToCheck = ["/Volumes/JorjaEEG/cs791_filtered/fif_Version/"]

sessionData = []
filename = []

#Where to save the data
filePath = "/Volumes/JorjaEEG/cs791_epoch/"
numpyPath = "/Volumes/JorjaEEG/cs791_epoch_numpy/"
psdsPath = "/Volumes/JorjaEEG/cs791_psds_numpy/"

#find files, make their path, and add to the list
for directory in dirsToCheck:
    dirFiles = os.listdir(directory)
    for file in dirFiles:
        if ".fif" in file:
            print(file)
            sessionData.append(os.path.join(directory,file))
            filename.append(file)
            

count = 0
total = 84 #total number of files
#load in the data
for subject in filename:
    file = sessionData[count]
    count += 1 #keep track of the number of participants, indexing starts @ 0
    raw = mne.io.read_raw_fif(file, preload = "True")
    #raw.copy().pick_types(meg=False, stim=True).plot(start=3, duration=12)
    events = mne.find_events(raw)
    
    #calc the ica
    epochs = mne.Epochs(raw, events, event_id = dict(eyesClosed=3), 
                        tmin=-5, tmax = 180,  preload = True)
    
    epochAve = epochs.average()
    
    #save the epoch data
    outputName = filePath + subject[:-4] + "-epoch.fif"
    
    epochs.save(fname = outputName, overwrite = True)
    
    numpyVersion = epochs.get_data()
    outputName = numpyPath + subject[:-4] + "-epoch.npy"
    np.save(outputName, arr = numpyVersion)
    
    numpyVersion = epochAve
    outputName = numpyPath + subject[:-4] + "-epochAve.npy"
    np.save(outputName, arr = numpyVersion)
    
    #Run the power analysis for each electrode
    tmin = 1 #set time for power analysis
    tmax = 180
    fmin = 0.5
    fmax = 100
    sfreq = epochs.info['sfreq']
    
    for channel in raw.ch_names:
        if not("E" in channel) or ("257" in channel):
            continue
        psds, freqs = mne.time_frequency.psd_welch(
            epochs,
            n_fft=int(sfreq * (tmax - tmin)),
            n_overlap=0, n_per_seg=None,
            tmin=tmin, tmax=tmax,
            fmin=fmin, fmax=fmax,
            verbose=False,
            picks = channel)
        
        outputName = psdsPath + subject[:-4] + "-" + channel + "-psds.npy"
        np.save(outputName, arr = psds)
    
        outputName = psdsPath + subject[:-4] + "-" + channel + "-freq.npy"
        np.save(outputName, arr = freqs)
    
    #run general overall power analysis
    psds, freqs = mne.time_frequency.psd_welch(
            epochs,
            n_fft=int(sfreq * (tmax - tmin)),
            n_overlap=0, n_per_seg=None,
            tmin=tmin, tmax=tmax,
            fmin=fmin, fmax=fmax,
            verbose=False,
            picks = list(range(1,257)))
    
    #uncomment to see plot of power analysis results for each participant
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
    
    
    #Save power analysis results
    outputName = psdsPath + subject[:-4] + "-psds.npy"
    np.save(outputName, arr = psds)
    
    outputName = psdsPath + subject[:-4] + "-freq.npy"
    np.save(outputName, arr = freqs)
    
    print("Done with", count, "out of", total, "and ", total-count, "left.")
    print("[][][][][][][][][][][][][][][][][][][][]")