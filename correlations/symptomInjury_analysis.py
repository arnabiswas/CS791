import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import shapiro
import scipy.stats as stats


pd.set_option('display.max_columns', None)
dfinjury = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\symptomTimeInjury.csv')

#droping all empty vlues
dfinjury.dropna(axis=0, inplace=True)
dfinjury.drop('ID', inplace=True, axis=1)
dfinjury.drop('Check', inplace=True, axis=1)

corrs = dfinjury.corr()#correlations
#sns.heatmap(corrs, yticklabels=True, xticklabels=True)
#plt.show()  
#print (corrs['Group'])

injury_corr = pd.DataFrame(corrs)
#print(current_corr)

#Behavioral data correlations

##Applying upper and lower thresholds for correlations and storing them in dataframes
dfupper = pd.DataFrame(injury_corr[np.abs(injury_corr["zScore"]) < .9])
dfclean = pd.DataFrame(dfupper[np.abs(dfupper["zScore"]) > .1])
###print (dfclean['Group'])

injuryset = pd.DataFrame(dfclean['zScore'])
#print(injuryset)
#sns.heatmap(injuryset, yticklabels=True, annot=True)
#plt.show()
#plt.close()

#Group correlations

##Applying upper and lower thresholds for correlations and storing them in dataframes
dfupper2 = pd.DataFrame(injury_corr[np.abs(injury_corr["Group"]) < .9])
dfclean2 = pd.DataFrame(dfupper2[np.abs(dfupper2["Group"]) > .1])
##print (dfclean['Group'])

injuryset2 = pd.DataFrame(dfclean2['Group'])
#print(injuryset2)
#sns.heatmap(injuryset2, yticklabels=True, annot=True)
#plt.show()
#.close()

#LOC correlations

##Applying upper and lower thresholds for correlations and storing them in dataframes
dfupper3 = pd.DataFrame(injury_corr[np.abs(injury_corr["Headache"]) < .9])
dfclean3 = pd.DataFrame(dfupper3[np.abs(dfupper3["Headache"]) > .1])
##print (dfclean['LOC'])

injuryset3 = pd.DataFrame(dfclean3['Headache'])
#print(injuryset3)
#sns.heatmap(injuryset3, yticklabels=True, annot=True)
#plt.show()
#plt.close()


#Separating zScore dataset by LOC classification, testing for assumptions and running a T-Test

a= dfinjury['Headache']
b= dfinjury['zScore']
print(a)
print(b)

#remove catagorical variables and unnecesary variab

#not Gaussian
stat, p = shapiro(a)
print('Statistics=', stat, 'pval=', p)
alpha = 0.05
if p > alpha:
	print('A is Gaussian')
else:
    print('A is not Gaussian')

stat, p = shapiro(b)
print('Statistics=', stat, 'pval=', p)
if p > alpha:
	print('B is Gaussian')
else:
    print('B is not Gaussian')
#no homogeneity of variance

stat2, p2 = stats.bartlett(a,b)
print(stat2,p2)
if p2 > alpha:
	print('Pass')
else:
    print('Fail')


