# -*- coding: utf-8 -*-
"""
Created on Fri May  4 22:00:59 2018

@author: me
"""
#this processes Austin Powers scripts, isolating quotes attributed to Dr. Evil, and then assigns quotes a cluster by kmeans based on dialogue before and after Dr. Evil quote.
from bs4 import BeautifulSoup
import requests
import pandas
import datetime
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

remove=['(', ')']
url="http://www.dailyscript.com/scripts/Austin_Powers_IMM.html"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
script=soup.find('pre').get_text()
regex = re.compile("\((.*?)\)")
result = re.sub(regex,'', script)
drevil_test=result.split("\r\n\r\n")


newlist=[]
for x in drevil_test:
    x=re.sub('\s+', ' ', x)
    x=x.replace("\r\n","")
    x=x.replace("&emdash","")
    x=x.split(" ")
    newlist.append(x[1:])

url2="http://www.dailyscript.com/scripts/Austin_Powers_TPWSM.html"
response2 = requests.get(url2)
html2 = response2.text

soup2 = BeautifulSoup(html2, "html.parser")
script2=soup2.find('pre').get_text()
result2 = re.sub(regex,'', script2)

drevil_test2=result2.split("\r\n\r\n")
newlist2=[]
for x in drevil_test2:
    x=re.sub('\s+', ' ', x)
    x=x.replace("\r\n","")
    x=x.replace("&emdash","")
    x=x.split(" ")
    x=x[1:]
    newlist2.append(x)
    
print(newlist2[13])

combined=newlist+newlist2
print(combined[12])
drevil=[]
before1=[]
before2=[]
after1=[]
after2=[]
alltext=[]
length=len(combined)
count2=0
while count2<length:
    if len(combined[count2])>2:
        if combined[count2][0]=='DR.' and combined[count2][1]=='EVIL':
            alltext.append(combined[count2]+combined[count2-1]+combined[count2-2]+combined[count2+1]+combined[count2+2])
            drevil.append(combined[count2])
            before1.append(combined[count2-1])
            before2.append(combined[count2-2])
            after1.append(combined[count2+1])
            after2.append(combined[count2+2])
    count2+=1

#join
count3=0
sentences=[]
while count3<len(alltext):
    sentences.append(' '.join(alltext[count3]))
    count3+=1

#saves quotes and contextual quotes in DF
DF = pandas.DataFrame({'drevil': drevil,'context':sentences})
DF.to_pickle("C:/Users/me/Documents/Python Scripts/bot/drevil_input")

#feature creation via kmeans
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(sentences)
model = KMeans(n_clusters=50, init='k-means++', max_iter=100, n_init=1)
labels=model.fit_predict(X)

#predict feature based on inputted text.  in application this will be tweet.
test=['whats the weather?']
test=vectorizer.transform(test)
print(model.predict(test))
















