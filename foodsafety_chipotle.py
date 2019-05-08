# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 11:10:26 2018

@author: me
"""
#scrapes iwaspoisoned.com and counts self-reports on chipotle food poisoning outbreaks, then updates historical record

from bs4 import BeautifulSoup
import pandas
import datetime, time
import urllib

today = datetime.date.today()
#historical record
history=pandas.read_csv("filepath.csv")

#get most recent data
url="https://iwaspoisoned.com/tag/chipotle-mexican-grill/"

try:
    user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent': user_agent}
    req=urllib.request.Request(url, headers=headers)
    response=urllib.request.urlopen(req)

except urllib.error.URLError as e:
    print(e)
    time.sleep(30)
    response.close()
else:
    html=(response.read())
    response.close()

soup=BeautifulSoup(html, "html.parser")
container=soup.find_all("li")#,

target='https://iwaspoisoned.com/tag/chipotle-mexican-grill?page='

#get number of pages of reported incidences
container2=[]
for x in container:
    if target in str(x):
        container2.append(x)
page=(len(container2))

#scrape page by page
page_count=0
while page_count<page:
    page_target=target+str(page)
    try:
        user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent': user_agent}
        req=urllib.request.Request(page_target, headers=headers)
        response=urllib.request.urlopen(req)

    except urllib.error.URLError as e:
        print(e)
        time.sleep(30)
        response.close()
    else:
        html=(response.read())
    #        print(html)
        response.close()
    
    soup2=BeautifulSoup(html, "html.parser")
    reports=soup2.find_all("div", attrs={"class":"col-md-6 report-first-box"} )
    print(reports[0])
    print(len(reports))
    chipotle='Chipotle'
    count=0
    for x in reports:
        if chipotle in str(x): 
            date_report=str(x).split('</p>')[0]
            date_report=date_report.split('<p class="report-date">')[1]
            #convert from string to datetime format

            add=[today, date_report]
            print(count,date_report)
            if date_report in history['report'].tolist():
                print('already added')
            else:
                history.loc[-1] = add
                history.index = history.index + 1
                history=history.sort_index()  
        count+=1
    page-=1

#update historical record
history.to_csv("filepath.csv", index=False)


