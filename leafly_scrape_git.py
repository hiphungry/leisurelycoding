# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 11:10:26 2018

@author: me
"""
#scraper of leafly reviews to assess liklihood of being paid
from bs4 import BeautifulSoup
import requests
import pandas
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from itertools import cycle
from urllib3.exceptions import HTTPError
import time

#get dispensary list for specific state with leaf_dispensary.py
#disp_list=pandas.read_csv(#csv of dispensaries urls)
#url_list=disp_list['dispensaries']

#starting variables for aggregate data
dispense=[]
total_reviews=[]
avg_rating=[]

#starting variables for reviews data
dispense_id=[]
dispense_user_id=[]
dispense_date=[]
dispense_reviews=[]
dispense_ratings=[]

#user variables
user_id=[]
user_total_reviews=[]
user_ratings=[] #list of lists
user_reviews=[] #list of list
user_dates=[] #list of lists

#cycle through a list of proxies
proxies = pandas.read_csv(#csv of proxies)
proxy_pool = cycle(proxies['IP_PORT'])

count=1
#get data from each dispensary page
for z in url_list:
    #print(z)
    url=z
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=3)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    proxy = next(proxy_pool)

    try:
        response = session.get(url)#,proxies={"http": proxy, "https": proxy})
        print(response, z)
    except HTTPError:
        time.sleep(10)
#        page=page
        print('http error')
#    except httplib.IncompleteRead:
#        time.sleep(10)
#        page=page
#        print('incomplete read')

    code=response
#    code=requests.get(url)
    soup=BeautifulSoup(code.text, "html.parser")
#    print(soup)
    #record
    dispense.append(z)
    
#parse for total reviews
    short_url=url.replace('https://www.leafly.com','')+'reviews'
    all_script=soup.find_all("a", {"href": short_url})
    container=str(all_script[0])
    container = container.split('<!-- -->')
    container = container[0].split('>')
    #record
    total_reviews.append(container[1])
    
#parse for avg rating
    all2_script=soup.find_all("span", {"class":"jsx-1187146964 avg-rating"})
    container=str(all2_script[0])
    container=container.split('</span>')
    container=container[0].split('>')
    avg_rating.append(container[1])

#get all reviews for each dispensary

#get last page
    review_url1=url+'reviews/?review-page=1'
    code2=requests.get(review_url1)
    soup2=BeautifulSoup(code2.text, "html.parser")
    lastpage=soup2.find_all("div", {"class":"jsx-2824115563 page-label"})
#print(lastpage)
    container=str(lastpage[0])
    container=container.split('of <!-- -->')
    container=container[1].split('</div>')
    lastpage=int(container[0])


#get user reviews by page
#put in while loop count < lastpage
    page=1
    while page<(lastpage+1):
        #print(z, page)
        review_url=url+'reviews/?review-page='+str(page)
#increase connection attempts, increase time between requests if error, rotate proxies
        session = requests.Session()
        retry = Retry(connect=10, backoff_factor=3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        proxy = next(proxy_pool)

        try:
            response = session.get(review_url)#,proxies={"http": proxy, "https": proxy})
#            print(response, page)
#            print(response.json())
        except HTTPError:
            time.sleep(10)
            page=page
            print('http error')
#        except httplib.IncompleteRead:
#            time.sleep(10)
#            page=page
#            print('incomplete read')

        code3=response
#        code3=requests.get(review_url)
        soup3=BeautifulSoup(code3.text, "html.parser")
#        print(soup3)

#get user
        user=soup3.find_all("a", {"class": "jsx-4225519787"})
#        print(user)
        for x in user:
            if "<img class" in str(x):
                user.remove(x)
        for x in user:
            usertest=str(x)
            usertest=usertest.split('href="')
            usertest=usertest[1].split('">')
            dispense_user_id.append(usertest[0])
            dispense_id.append(z)

#<div class="jsx-4225519787 date-desktop">2018-4-17</div>
        #get date
        date=soup3.find_all("div", {"class":"jsx-4225519787 date-desktop"})
        for x in date:
            date=str(x)
            date=date.split('date-desktop">')
            date=date[1].split('</div>')
            dispense_date.append(date[0])
#print(date[0])

#get text of reviews <div col="12" col-lg="11" class="jsx-4225519787">
        reviews_text=soup3.find_all("div", {"class":"jsx-4225519787", "col":"12", "col-lg":"11"})
        for x in reviews_text:
            if "thumb-icon-container" in str(x):
                reviews_text.remove(x)
#print(reviews_text)
#print(len(reviews_text))
        for x in reviews_text:
            rtext=str(x)
            rtext=rtext.split('col-lg="11">')
            rtext=rtext[1].split('</div>')
            dispense_reviews.append(rtext[0])

#get rating for the review <div class="jsx-4225519787 star-text">
        stars=soup3.find_all("div", {"class":"jsx-4225519787 star-text"})
        for x in stars:
            star=str(x)
            star=star.split('star-text">')
            star=star[1].split('</div>')
            dispense_ratings.append(star[0])
#            print(dispense_ratings)
        
        print(z,page)        
        page+=1

#write interim data
    d={'dispense_id':dispense_id, 'dispense_user_id':dispense_user_id, 'dispense_reviews':dispense_reviews, 'dispense_date': dispense_date, 'dispense_ratings': dispense_ratings}
    df = pandas.DataFrame(data=d)
    write_url="#path"+str(count)+".csv"
    df.to_csv(write_url, index=False)
    count+=1

#write summary data
data_df={'dispense_id':dispense, 'total_reviews':total_reviews, 'avg_rating':avg_rating}
df = pandas.DataFrame(data=data_df)
df.to_csv("#path+/dispensaries_data.csv", index=False)

