import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


#Import dataset (At time of testing)
pd.set_option('display.max_columns', None)
dfinjuryCurrent = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\symptomCurrent.csv')

#droping all empty vlues
dfinjuryCurrent.dropna(axis=0, inplace=True)
dfinjuryCurrent.drop('ID', inplace=True, axis=1)
dfinjuryCurrent.drop('LOC', inplace=True, axis=1)


#Initial corr map. NOT USED
#corrs = dfinjuryCurrent.corr()#correlations
#sns.heatmap(corrs, yticklabels=True, xticklabels=True)
#plt.show()  
#print (corrs['Group'])


#Corr. and pval calculation
dfcorr2 = pd.DataFrame() # Correlation matrix
dfp2 = pd.DataFrame()
for x in dfinjuryCurrent :
    for y in dfinjuryCurrent :
       corr2,pval2 = stats.spearmanr(dfinjuryCurrent[x], dfinjuryCurrent[y])
       dfcorr2.loc[x,y] = corr2
       dfp2.loc[x,y] = pval2
#print(dfcorr2)
#print(dfp2)
dfcorr2.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\dfcorr2check.csv')


#Data exclusion
dfupperg2 = pd.DataFrame(dfcorr2[np.abs(dfcorr2["Group"]) < .9])
cleancorrg2 = pd.DataFrame(dfupperg2[np.abs(dfupperg2["Group"]) > .1])
cleanpvalg2 = pd.DataFrame(dfp2[dfp2["Group"] < .05])
print(cleanpvalg2['Group'])
print(cleancorrg2['Group'])
cleancorrg2.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorr1Current.csv')
cleanpvalg2.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpval1Current.csv')
#print(cleancorrg2)

dfupperz2 = pd.DataFrame(dfcorr2[np.abs(dfcorr2["zScore"]) < .9])
cleancorrz2 = pd.DataFrame(dfupperz2[np.abs(dfupperz2["zScore"]) > .1])
cleanpvalz2 = pd.DataFrame(dfp2[dfp2["zScore"] < .05])
print(cleanpvalz2['zScore'])
print(cleancorrz2['zScore'])
cleancorrz2.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorr2Current.csv')
cleanpvalz2.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpval2Current.csv')
#print(cleancorrz2)


###############
###############


#Import dataset (At time of injury)
pd.set_option('display.max_columns', None)
dfinjuryInjury = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\symptomTimeInjury.csv')

#droping all empty vlues
dfinjuryInjury.dropna(axis=0, inplace=True)
dfinjuryInjury.drop('Check', inplace=True, axis=1)
dfinjuryInjury.drop('ID', inplace=True, axis=1)
dfinjuryInjury.drop('LOC', inplace=True, axis=1)


#Initial corr map. NOT USED
#corrs = dfinjuryInjury.corr()#correlations
#sns.heatmap(corrs, yticklabels=True, xticklabels=True)
#plt.show()  
#print (corrs['Group'])


#Corr. and pval calculation
dfcorr = pd.DataFrame() # Correlation matrix
dfp = pd.DataFrame()
for x in dfinjuryInjury :
    for y in dfinjuryInjury :
       corr,pval = stats.spearmanr(dfinjuryInjury[x], dfinjuryInjury[y])
       dfcorr.loc[x,y] = corr
       dfp.loc[x,y] = pval
#print(dfpval)
#print(dfp)
dfcorr.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\dfcorrcheck.csv')

#Data exclusion
dfupperg = pd.DataFrame(dfcorr[np.abs(dfcorr["Group"]) < .9])
cleancorrg = pd.DataFrame(dfupperg[np.abs(dfupperg["Group"]) > .1])
cleanpvalg = pd.DataFrame(dfp[dfp["Group"] < .05])
print(cleanpvalg['Group'])
print(cleancorrg['Group'])
cleancorrg.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorr1Injury.csv')
cleanpvalg.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpval1Injury.csv')
#print(cleancorgr)

dfupperz = pd.DataFrame(dfcorr[np.abs(dfcorr["zScore"]) < .9])
cleancorrz = pd.DataFrame(dfupperz[np.abs(dfupperz["zScore"]) > .1])
cleanpvalz = pd.DataFrame(dfp[dfp["zScore"] < .05])
print(cleanpvalz['zScore'])
print(cleancorrz['zScore'])
cleancorrz.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorr2Injury.csv')
cleanpvalz.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpval2Injury.csv')
#print(cleancorrz)

dfupperh = pd.DataFrame(dfcorr[np.abs(dfcorr["Headache"]) < .9])
cleancorrh = pd.DataFrame(dfupperz[np.abs(dfupperz["Headache"]) > .1])
cleanpvalh = pd.DataFrame(dfp[dfp["Headache"] < .05])
print(cleanpvalh['Headache'])
print(cleancorrh['Headache'])
cleancorrh.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleancorr3Injury.csv')
cleanpvalh.to_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\cleanpval3Injury.csv')
#print(cleancorrz)

