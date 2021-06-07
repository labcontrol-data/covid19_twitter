#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 8 17:55:39 2021

@author: vargas

Author: Alessandro N. Vargas
Website: www.anvargas.com
Email: avargas@utfpr.edu.br

Note: The Covid database is available at
 https://github.com/thepanacealab/covid19_twitter
Dr. Juan Banda and colleagues created this database, and it allows us 
to download more than a billion Covid-related tweets. We applied a 
routine to extract from this billion of tweets only the tweets written 
in English. Next, we searched for negative words. We saw that some 
negative words were common in Covid-related tweets, such as 'panic', 
'hate', among others. We then selected the most common negative 
words (see the 'database' below), and we counted the number of 
occurrences of those negative words daily. Run this code to generate 
the 'negative index', that is, the number of negative words counted 
each day. It will help if you define the start and end dates. 
Pay attention to set the correct start and end dates.
"""
import pandas as pd
import datetime
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.available


###########################################################################
# create urls to be downloaded
def insertStr(datex):
    texto1 = 'https://raw.githubusercontent.com/labcontrol-data/covid19_twitter/main/dailies/'
    texto2 = '_negative_terms.csv'
    return texto1 + datex + '/' + datex + texto2

# variable `linkDB' is a database containing all urls
linkDB=[]; 

# variable `linkDB' is a database containing all dates under study
dateDB=[];
d1 = datetime.date(2020,3,1)    # start date: 2020-3-22 
d2 = datetime.date(2021,6,2)    # end date: 2021-6-2
diff = d2 - d1
for i in range(diff.days + 1):
    date_str = (d1 + datetime.timedelta(i)).isoformat()
    linkDB.append(insertStr(date_str))  #creates the address link database
    dateDB.append(date_str)             #creates the database of dates
    #print( insertStr(date_str) )

listWords=[];

# creates a dictionary structure to record all the occurences of negative words for each day
dictDB = pd.DataFrame(columns=['date', 'ocurrences'])

for d in range(0,len(linkDB)):
    date_str = dateDB[d]
    print('Day covered: ', date_str )
    url = linkDB[d]
    df = pd.read_csv(url, error_bad_lines=True)
    ocurrences = df.ocurrences.sum()
    john = pd.Series(data=[date_str,ocurrences],
                      index=dictDB.columns)
    dictDB = dictDB.append(john,ignore_index=True)


graph=dictDB.plot(x = 'date', y = 'ocurrences', figsize = (14,6), linewidth = 4, color = 'black', legend = False)
graph.tick_params(axis = 'both', which = 'major', labelsize = 18)
graph.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
graph.text(x = 100, y = 88000, s = 'Number of negative words in tweets', color = 'blue', weight = 'bold', rotation = 0,
              backgroundcolor = 'white', fontsize = 26)
plt.tight_layout()
plt.savefig("negativeCovidFinal.pdf")

# This database below contain the information to generate
# the 'negative index'
dictDB.to_csv('databaseNegativeFinal.csv', index = False)


listNegativeWords  = list(dict.fromkeys(df['words']))
print('\n Negative words in the database:\n')
print(listNegativeWords)


###########################################################################
# Procedure to create a database with the number of tweets in English
###########################################################################

def insertStrID(datex):
    texto1 = 'https://raw.githubusercontent.com/labcontrol-data/covid19_twitter/main/dailies/'
    texto2 = '_tweets_ID.tsv'
    return texto1 + datex + '/' + datex + texto2


# variable `linkDB' is a database containing all urls
linkDB=[]; 

# variable `linkDB' is a database containing all dates under study
dateDB=[];
d1 = datetime.date(2020,3,1)     # start date: 2020-3-22
d2 = datetime.date(2021,6,2)     # end date: 2021-6-2
diff = d2 - d1
for i in range(diff.days + 1):
    date_str = (d1 + datetime.timedelta(i)).isoformat()
    linkDB.append(insertStrID(date_str))  #creates the address link database
    dateDB.append(date_str)             #creates the database of dates
    #print( insertStrID(date_str) )

# creates a dictionary structure to record the number of  tweets in English
# the element 'rate' informs us what is the share of English among all idioms
dictQuan = pd.DataFrame(columns=['date', 'ocurrences', 'rate'])


for d in range(0,len(linkDB)):    
    date_str = dateDB[d]
    print('Day covered_ID: ', date_str )
    fileN = linkDB[d] 
    df = pd.read_csv(fileN,sep='\t')

    countEnglish = len(df[df['lang'] == "en"])

    ocurrences = countEnglish
    ratex = ocurrences/len(df)
    john = pd.Series(data=[date_str,ocurrences, ratex],
                        index=dictQuan.columns)
    dictQuan = dictQuan.append(john,ignore_index=True)


dictQuan.to_csv('databaseOcurrencesEnglishFinal.csv', index = False)
