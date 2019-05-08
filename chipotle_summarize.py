# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 21:23:33 2019

@author: me
"""

#summarizes scrape of iwaspoisoned.com

import pandas
from collections import Counter
import datetime

#raw scrape data
history=pandas.read_csv("filepath/chipotle_raw.csv")

#query and remove 'nan' or empty days
reports = [x for x in history['report'] if str(x) != 'nan']

instances=[]
for x in reports:
    instance=str(x).split(' ')
    instance=instance[0]+'_'+instance[1]+'_'+instance[2]
    date=datetime.datetime.strptime(instance,'%b_%d_%Y')
    instances.append(date)

counts=Counter(instances)

date=[]
count=[]

for d, c in counts.items():
    date.append(d)
    count.append(c)

#record number of instances
data={'date':date, 'frequency':count}
df=pandas.DataFrame(data)
df=df.sort_values(by='date')
df=df.reset_index(drop=True)


df.to_csv("chipotle_summary.csv", index=False)
