import pandas as pd
import matplotlib.pyplot as plt


#Graphing barplots: corr at Injury
dfcorrgraphg = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrgInjury.csv')
dfcorrgraphz = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrzInjury.csv')
dfcorrgraphh = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrhInjury.csv')


#Group corr
xcorrg = dfcorrgraphg["Symptom"]
ycorrg = dfcorrgraphg["Group"]

fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(dpi=300)
corrgraphg = plt.barh(xcorrg,ycorrg)

plt.axvline(x=0,linewidth=1, color='k')
plt.xlabel("Correlation Coefficient (ρ)")
plt.ylabel("Symptoms")
plt.title("Injury Symptoms to Subgroup")
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30)

for index, value in enumerate(ycorrg):
    if value > 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='right',verticalalignment='center')
    elif value < 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='left',verticalalignment='center')
 
plt.show()
plt.close()

#zScore corr     
xcorrz = dfcorrgraphz["Symptom"]
ycorrz = dfcorrgraphz["zScore"]

fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(dpi=300)
corrgraphg = plt.barh(xcorrz,ycorrz)

plt.axvline(x=0,linewidth=1, color='k')
plt.xlabel("Correlation Coefficient (ρ)")
plt.ylabel("Symptoms")
plt.title("Injury Symptoms to VWM Performance")
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30)

for index, value in enumerate(ycorrz):
    if value > 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='right',verticalalignment='center')
    elif value < 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='left',verticalalignment='center')
 
plt.show()
plt.close()

#xcorrh = dfcorrgraphh["Symptom"]
#ycorrh = dfcorrgraphh["Group"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#corrgraphh = plt.bar(xcorrh,ycorrh, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("Correlation Coefficient (ρ)")
#plt.title("Injury Symptoms to Headache")
#plt.show()
#plt.close()


#Graphing barplots: pval at Injury
#dfpvalgraphg = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalgInjury.csv')
#dfpvalgraphz = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalzInjury.csv')
#dfpvalgraphh = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalhInjury.csv')

#xpvalg = dfpvalgraphg["Symptom"]
#ypvalg = dfpvalgraphg["Group"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphg = plt.bar(xpvalg,ypvalg, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to Subgroup")
#plt.show()
#plt.close()

#xpvalz = dfpvalgraphz["Symptom"]
#ypvalz = dfpvalgraphz["zScore"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphz = plt.bar(xpvalz,ypvalz, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to VWM Performance")
#plt.show()
#plt.close()

#xpvalh = dfpvalgraphh["Symptom"]
#ypvalh = dfpvalgraphh["Group"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphh = plt.bar(xpvalh,ypvalh, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to Headache")
#plt.show()
#plt.close()


#############
#############


#Graphing barplots: corr at Current
dfcorrgraphg2 = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrgCurrent.csv')
dfcorrgraphz2 = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrzCurrent.csv')
dfcorrgraphLOC = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorrLOCCurrent.csv')


#Group corr
xcorrg2 = dfcorrgraphg2["Symptom"]
ycorrg2 = dfcorrgraphg2["Group"]


fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(dpi=300)
corrgraphg2 = plt.barh(xcorrg2,ycorrg2)

plt.axvline(x=0,linewidth=1, color='k')
plt.xlabel("Symptoms")
plt.ylabel("Correlation Coefficient (ρ)")
plt.title("Current Symptoms to Subgroup")
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30)

for index, value in enumerate(ycorrg2):
    if value > 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='right',verticalalignment='center')
    elif value < 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='left',verticalalignment='center')
      
plt.show()
plt.close()

#zScore corr     
xcorrz2 = dfcorrgraphz2["Symptom"]
ycorrz2 = dfcorrgraphz2["zScore"]


fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(dpi=300)
corrgraphz2 = plt.barh(xcorrz2,ycorrz2)

plt.axvline(x=0,linewidth=1, color='k')
plt.xlabel("Symptoms")
plt.ylabel("Correlation Coefficient (ρ)")
plt.title("Current Symptoms to VWM Performance")
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30)

for index, value in enumerate(ycorrz2):
    if value > 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='right',verticalalignment='center')
    elif value < 0 :
        plt.text(value, index, str(round(value,3)),horizontalalignment='left',verticalalignment='center')
        
plt.show()
plt.close()
    
        
#xcorrLOC = dfcorrgraphLOC["Symptom"]
#ycorrLOC = dfcorrgraphLOC["LOC"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#corrgraphLOC = plt.bar(xcorrLOC,ycorrLOC, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("Correlation Coefficient (ρ)")
#plt.title("Current Symptoms to LOC")
#plt.show()
#plt.close()


#Graphing barplots: pval at Injury
#dfpvalgraphg2 = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalgCurrent.csv')
#dfpvalgraphz2 = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalzCurrent.csv')
#dfpvalgraphLOC = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpvalLOCCurrent.csv')

#xpvalg2 = dfpvalgraphg2["Symptom"]
#ypvalg2 = dfpvalgraphg2["Group"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphg2 = plt.bar(xpvalg2,ypvalg2, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to Subgroup")
#plt.show()
#plt.close()

#xpvalz2 = dfpvalgraphz2["Symptom"]
#ypvalz2 = dfpvalgraphz2["zScore"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphz2 = plt.bar(xpvalz2,ypvalz2, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to VWM Performance")
#plt.show()
#plt.close()

#xpvalLOC = dfpvalgraphLOC["Symptom"]
#ypvalLOC = dfpvalgraphLOC["LOC"]

#plt.figure(figsize=(30, 15))
#plt.plot(dpi=300)
#pvalgraphLOC = plt.bar(xpvalLOC,ypvalLOC, width=.7)

#plt.axhline(y=0,linewidth=1, color='k')
#plt.xlabel("Symptoms")
#plt.ylabel("p-value")
#plt.title("Injury Symptoms to LOC")
#plt.show()
#plt.close()