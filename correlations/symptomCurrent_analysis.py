import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.multivariate.manova import MANOVA
from scipy.stats import shapiro
import scipy.stats as stats
import scikit_posthocs as sp
import statistics

pd.set_option('display.max_columns', None)
dfinjury = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\symptomCurrent.csv')

#droping all empty vlues
dfinjury.dropna(axis=0, inplace=True)
dfinjury.drop('ID', inplace=True, axis=1)

corrs = dfinjury.corr()#correlations
#sns.heatmap(corrs)
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
#plt.close()

#LOC correlations

##Applying upper and lower thresholds for correlations and storing them in dataframes
dfupper3 = pd.DataFrame(injury_corr[np.abs(injury_corr["LOC"]) < .9])
dfclean3 = pd.DataFrame(dfupper3[np.abs(dfupper3["LOC"]) > .1])
#print (dfclean3['LOC'])

injuryset3 = pd.DataFrame(dfclean3['LOC'])
#print(injuryset3)
#sns.heatmap(injuryset3, yticklabels=True, annot=True)
#plt.show()
#plt.close()


#Separating zScore dataset by LOC classification, testing for assumptions and running a T-Test
LOC = dfinjury[dfinjury['LOC'] == 1]
no_LOC = dfinjury[dfinjury['LOC'] == 0]

a= LOC['zScore']
b= no_LOC['zScore']
print(a)
print(b)

#remove catagorical variables and unnecesary variab

#Gaussian
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
#homogeneity of variance

stat2, p2 = stats.bartlett(a,b)
print(stat2,p2)
if p2 > alpha:
	print('Pass')
else:
    print('Fail')


fit = stats.ttest_ind(a, b, alternative='greater')
print('T-test Results:',fit)
print(statistics.mean(a),(statistics.mean(b)))
      
SD = statistics.math.sqrt((statistics.stdev(a))**2 + (statistics.stdev(b))**2)
CohensD = ((statistics.mean(a)-statistics.mean(b))/(SD))
print("Cohen's D = ", CohensD)
if 0<=CohensD<0.1 :
        print("Very Small effect")
elif 0.1<=CohensD<0.35:
        print("Small effect")
elif 0.35<=CohensD<0.65:
        print("Medium effect")
elif 0.65<=CohensD<0.9:
        print("Large")
elif CohensD >= 0.9:
    print("Very Large effect")




#Violin Plot
figdata = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\LOC_zScores.csv')

ax = sns.boxplot(x = figdata['LOC'], y = figdata['zScore'], data = figdata)
plt.show()
plt.close()

fig, ax = plt.subplots(figsize=(6, 6))

# Titles
ax.set_title('zScore vs LOC')
ax.set_xlabel('LOC')
ax.set_ylabel('zScore')

# Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Adds major gridlines
ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.4)

#scatter = ax.scatter(b,dfinjury['zScore'], c=dfinjury['Group'])
#legend1 = ax.legend(*scatter.legend_elements(), loc="lower center", title="Group")
#plt.show()
#plt.close()

#plt.hist(a,bin=.2,color=b)
#plt.show()
#plt.close()