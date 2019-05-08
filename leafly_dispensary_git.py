# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:08:42 2018

@author: me
"""
#scrapes list of urls of dispensaries for california. can modify to search and record urls for dispensaries in any state

from bs4 import BeautifulSoup
import requests
import pandas

#get list
url="https://www.leafly.com/finder/california"
code=requests.get(url)
soup=BeautifulSoup(code.text, "html.parser")

#get all dispensariess list of urls
all_script=soup.find_all("a", {"class": "jsx-2127423489 view-menu-button"})

#parse arefs
dispensaries=[]
for x in all_script:
#print(all_script[0])
    reports_script=str(x)
    container = reports_script.split('href="')
    container=container[1].split('"')
    container=container[0].split('menu')
    dispensaries.append(container[0])
#    print(len(dispensaries))
#print(dispensaries)

df = pandas.DataFrame(dispensaries, columns=['dispensaries'])
    
df.to_csv("#filepath+/dispensaries.csv", index=False)

