import pandas as pd
from scipy.stats import chi2_contingency
import math


pd.set_option('display.max_columns', None)
dfcurrent = pd.read_csv(r'C:\Users\Rdurb\OneDrive\Documents\mTBI_project\mTBI_data\symptomCurrent.csv')
twosub_loc = pd.crosstab(index=dfcurrent['Group'], columns=dfcurrent['LOC'])
print(twosub_loc)
#Chi squared
stat, p, dof, expected = chi2_contingency(twosub_loc)
print(stat, p , dof)

#Effect size
n = 103
phi = math.sqrt(stat/n)
print('effect size = ', phi)
