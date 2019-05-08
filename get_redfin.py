# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 10:31:03 2018

@author: me
"""
#gets list of addresses from redfin, then scrapes redfin estimate for a sample of the properties, summarizing scraped redfin estimate on per sq ft basis, then gets mean price for all properties listed sold or listed for sales

import pandas
from bs4 import BeautifulSoup
import urllib
import time
import random
import datetime
import numpy as np
import csv
from io import StringIO

history_data=pandas.read_csv("#filepath+redfin_history.csv")

#sample
size='5000'
url="https://www.redfin.com/stingray/api/gis-csv?al=1&market=socal&min_stories=1&num_homes="+size+"&ord=redfin-recommended-asc&page_number=1&region_id=9361&region_type=6&sf=1,2,3,5,6,7&sold_within_days=365&status=9&uipt=1,2,3,4,5,6&v=8"

try:
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent': user_agent}
    req=urllib.request.Request(url, headers=headers)
    response=urllib.request.urlopen(req).read()
    b = response.decode('utf8')
    f = StringIO(b)
    reader = csv.reader(f, delimiter=',')
    data = []
    for row in reader:
        data.append(row)
    length=len(data)-2
    df = pandas.DataFrame(data[1:(length+1)], columns=data[0])

except urllib.error.URLError as e:
    print(e)
    time.sleep(60)
else:
    print('not open')

df=df.loc[df['SQUARE FEET'] != '']
df=df.loc[df['$/SQUARE FEET'] != '']
df=df.loc[df['DAYS ON MARKET'] != '']
df=df.reset_index(drop=True)
length2=len(df['SQUARE FEET'])
rsample = random.sample(range(0,length2), 200)
df=df.astype({'SQUARE FEET':int})

count=0
redfin_est=[]
for x in rsample:
    try:
        print(x, length2)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent': user_agent}
        req=urllib.request.Request(df['URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'][x], headers=headers)
        response=urllib.request.urlopen(req)
        print(df['URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'][x])
        time.sleep(5)

    except urllib.error.URLError as e:
        print(e)
        time.sleep(10)
        response.close()

    else:
        html=(response.read())
        response.close()
        soup=BeautifulSoup(html, "html.parser")
        container=str(soup.find_all("div", attrs={"class":"statsValue"})[0])#div 
        if ('<span>' in container):
            container=container.split('<span>')[2]
            container=container.split('</span>')[0]
            container=container.replace('+','')
            container=int(container.replace(',',''))
        elif('<span>' not in container):
            container=container.split('</div>')[0]
            container=container.split('>')[1]
            container=container.replace('+','')
            container=(container.replace('$',''))
            container=int(container.replace(',',''))
        else:
            print(df['STATUS'][x])
            container=np.nan
        if (np.isnan(df['SQUARE FEET'][x])):
            sqft=np.mean(df['SQUARE FEET'])
        else:
            sqft=df['SQUARE FEET'][x]
        doll_sqft=container/sqft
        redfin_est.append(doll_sqft)
        #count+=1
        print(type(container), container)
today = datetime.date.today()

df_active=df.loc[df['STATUS'] == 'Active']
df_sold=df.loc[df['STATUS'] == 'Sold']

est_sqft=np.mean(redfin_est)
est_sqft_stdv=np.nanstd(redfin_est)
est_cnt=len(redfin_est)

df_active=df_active.astype({'$/SQUARE FEET':float, 'DAYS ON MARKET':float})
active_sqft=np.mean(df_active['$/SQUARE FEET'])
active_sqft_stdv=np.nanstd(df_active['$/SQUARE FEET'])
active_days=np.mean(df_active['DAYS ON MARKET'])
active_days_stdv=np.nanstd(df_active['DAYS ON MARKET'])
active_cnt=len(df_active['$/SQUARE FEET'])
df_sold=df_sold.astype({'$/SQUARE FEET':float, 'DAYS ON MARKET':float})
sold_sqft=np.mean(df_sold['$/SQUARE FEET'])
sold_sqft_stdv=np.nanstd(df_sold['$/SQUARE FEET'])
sold_days=np.mean(df_sold['DAYS ON MARKET'])
sold_days_stdev=np.nanstd(df_sold['DAYS ON MARKET'])
sold_cnt=len(df_sold['$/SQUARE FEET'])

add=[today, est_sqft, est_sqft_stdv, est_cnt, active_sqft, active_sqft_stdv, active_days, active_days_stdv, active_cnt, sold_sqft, sold_sqft_stdv, sold_cnt]
history_data.loc[-1] = add  # adding a row
history_data.index = history_data.index + 1  # shifting index
history_data = history_data.sort_index()  
history_data.to_csv("#filepath+redfin_history.csv", index=False)
