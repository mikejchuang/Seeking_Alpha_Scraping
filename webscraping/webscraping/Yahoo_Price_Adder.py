from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from yahoo_quote_download import yqd
import numpy as np
import time
import csv
import random
import re

# for processing initial CSV
# saurl = pd.read_csv('/Users/michaelchuang/git_project/mjc_WebScraping/Lightning_round_URLS1.csv')
# saurl = saurl.drop('TITLE.1', axis=1)
# saurl['DATE'] = saurl.TITLE.str[-11:]
# saurl['DATE']= saurl['DATE'].str.split(' ').str[1]

su = pd.read_csv('/Users/michaelchuang/git_project/mjc_WebScraping/webscraping/lightning2.csv')
su['bearish'] = su.bearish.apply(lambda x: x[0:].split(','))
su['bullish'] = su.bullish.apply(lambda x: x[0:].split(','))

# remove bearish/bullish that are the same
j2=[]
for i in range(len(su.bullish)):
    if list(set(su.bullish[i]) - set(su.bearish[i]))==[]:
        j2.append(i)
su.drop(su.index[j2])

# remove duplicates in bullish
for i in range(len(su.bullish)):
    su.bullish[i]=list(set(su.bullish[i]) - set(su.bearish[i]))

# remove non ticker links
for i in range(len(su.bullish)):
     su.bullish[i]= [x for x in su.bullish[i] if x.startswith('https://seekingalpha.com/symbol/')]

# remove seeking alpha

for i in range(len(su.bullish)):
    su.bullish[i] = [x.lstrip('https://seekingalpha.com/symbol/') for x in su.bullish[i]]

# same for bearish
for i in range(len(su.bearish)):
     su.bearish[i]= [x for x in su.bearish[i] if x.startswith('https://seekingalpha.com/symbol/')]

for i in range(len(su.bearish)):
      su.bearish[i]= [x.lstrip('https://seekingalpha.com/symbol/') for x in su.bearish[i]]


su['date'] = [x[0:10] for x in su.date]
su['date']= pd.to_datetime(su['date'])
su['enddate'] = su['date']+pd.DateOffset(months=6)
su['date']= (su['date'].astype(str))
su['enddate']= su['enddate'].astype(str)
su['date']= su['date'].str.replace('-', '')
su['enddate']=su['enddate'].str.replace('-', '')


su['yqdopen']=np.empty((len(su.date), 0)).tolist()
su['yqdclose6m']=np.empty((len(su.date), 0)).tolist()
su['yqdclose30d']=np.empty((len(su.date), 0)).tolist()
su['yqdclose7d']=np.empty((len(su.date), 0)).tolist()

for i in range(len(su.bullish)):
    print('currently on row: ' + str(i))
    for j in range(len(su.bullish[i])):
        try:
            quote = (yqd.load_yahoo_quote(str(su.bullish[i][j]),su.date[i], su.enddate[i]))
            openq = quote[1].split(',')
            close7d = quote[7].split(',')
            close30d = quote[25].split(',')
            close6m = quote[-2].split(',')
        except:
            try:
                time.sleep(2)
                quote = (yqd.load_yahoo_quote(str(su.bullish[i][j]),su.date[i], su.enddate[i]))
                close7d = quote[7].split(',')
                close30d = quote[25].split(',')
                close6m = quote[-2].split(',')
            except:
                continue

        su['yqdopen'][i].append([openq[0],openq[-2]])
        su['yqdclose7d'][i].append([close7d[0],close7d[-2]])
        su['yqdclose30d'][i].append([close30d[0],close30d[-2]])
        su['yqdclose6m'][i].append([close6m[0],close6m[-2]])

        print(su.bullish[i])
        print(su.yqdopen[i])
        print(su.yqdclose7d[i])
        print(su.yqdclose30d[i])


su.to_csv('/Users/michaelchuang/git_project/mjc_WebScraping/webscraping/results3.csv')
