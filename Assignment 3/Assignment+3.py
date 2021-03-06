# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

import pandas as pd
import numpy as np


def get_Energy():
    energy = pd.read_excel('Energy Indicators.xls', skiprows =17, skip_footer=38)
    energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace =True)
    energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.replace('...', np.nan, inplace = True)
    energy['Energy Supply'] *= 1000000
    replace_dict = {'Country':{"Republic of Korea" : "South Korea", "United States of America": "United States", 
                           "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                          "China, Hong Kong Special Administrative Region": "Hong Kong"}}
    energy['Country'] = energy['Country'].apply(lambda name: name.split("(")[0].strip())
    energy['Country'] = energy['Country'].str.replace("\d+","")
    energy.replace(replace_dict, inplace = True)
    return energy


def get_GDP():
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    replace_dict = {"Country Name":{"Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"}}
    GDP.replace(replace_dict, inplace=True)
    GDP.rename(columns={"Country Name": "Country"}, inplace=True)
    return GDP


# now load sciamago data
def get_ScimEn():
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    return ScimEn


def answer_one():
    energy = get_Energy()
    GDP = get_GDP()
    ScimEn = get_ScimEn()
    dataSet = ScimEn.merge(energy, on="Country").merge(GDP, on="Country")
    dataSet.set_index('Country', inplace=True)
    output = dataSet[['Rank', 'Documents', 'Citable documents', 
              'Citations', 'Self-citations', 
              'Citations per document', 'H index', 
              'Energy Supply', 'Energy Supply per Capita', 
              '% Renewable', '2006', '2007', '2008', '2009', 
              '2010', '2011', '2012', '2013', '2014', '2015']]
    
    return output.head(15)


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

def answer_two():
    energy = get_Energy()
    GDP = get_GDP()
    ScimEn = get_ScimEn()
    dataSet = ScimEn.merge(energy, on="Country").merge(GDP, on="Country")
    n_dataSet = len(dataSet)
    energy_GDP = energy.merge(GDP, on="Country")
    GDP_ScimEn = GDP.merge(ScimEn, on="Country")
    ScimEn_energy = ScimEn.merge(energy, on="Country")
    n_energy, n_GDP, n_ScimEn = len(energy), len(GDP), len(ScimEn)
    n_energy_GDP, n_GDP_ScimEn, n_ScimEn_energy = len(energy_GDP), len(GDP_ScimEn), len(ScimEn_energy)
    n_GDP_energy_ScimEn = n_energy + n_GDP + n_ScimEn - n_energy_GDP - n_GDP_ScimEn - n_ScimEn_energy + n_dataSet
    return n_GDP_energy_ScimEn - n_dataSet


# Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*


def answer_three():
    Top15 = answer_one()
    Top15_GDP = Top15[['2006', '2007', '2008', '2009', '2010', 
                   '2011', '2012', '2013', '2014', '2015']]
    Top15_GDP['avgGDP'] = Top15_GDP.mean(axis=1)
    return Top15_GDP.sort('avgGDP', ascending=False)['avgGDP']


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*


def answer_four():
    Top15 = answer_one()
    Top15_GDP = Top15[['2006', '2007', '2008', '2009', '2010', 
                   '2011', '2012', '2013', '2014', '2015']]
    Top15_GDP['avgGDP'] = Top15_GDP.mean(axis=1)
    Top15_GDP.sort('avgGDP', ascending=False, inplace=True)
    sixth = Top15_GDP.iloc[5]
    return sixth['2015'] - sixth['2006']


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*


def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*


def answer_six():
    Top15 = answer_one()
    country = Top15['% Renewable'].idxmax()
    max_renewable = Top15.loc[country]
    return country, max_renewable['% Renewable']


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*


def answer_seven():
    Top15 = answer_one()
    Top15['Citations Ratio'] = Top15['Self-citations'] / Top15['Citations']
    country = Top15['Citations Ratio'].idxmax()
    return country, Top15.loc[country]['Citations Ratio']


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*


def answer_eight():
    Top15 = answer_one()
    Top15['pop'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15.sort('pop', ascending=False, inplace=True)
    Top15.reset_index(inplace=True)
    return Top15.iloc[2]['Country']


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*


def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*


def answer_ten():
    Top15 = answer_one()
    medianRV = Top15['% Renewable'].median()
    Top15['HighRenew'] = 0
    Top15['HighRenew'].where(Top15['% Renewable'] < medianRV, other=1, inplace=True)
    return Top15['HighRenew']


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*


def answer_eleven():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continents'] = pd.Series(ContinentDict)
    reduced = Top15[['Continents','PopEst']]
    output = reduced.groupby('Continents').PopEst.agg({'size':len, 'sum':np.sum, 'mean':np.mean, 'std':np.std})
    return output


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*


def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continents'] = pd.Series(ContinentDict)
    Top15['RenewBins'] = pd.cut(Top15['% Renewable'], 5)
    Top15.reset_index(inplace=True)
    return Top15.groupby(['Continents', 'RenewBins']).Country.count()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*


def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).apply(lambda x: "{:,}".format(x))
    return Top15['PopEst']


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

