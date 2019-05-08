# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 17:23:15 2018

@author: me
"""

#gets tweets associated with "chipotle" and "sick" to identify trends in food outbreaks, counts and updates historical record

import tweepy
from keys import keys
from datetime import timedelta, datetime
import pandas as pd
#from get_response import response

#get keys
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

#authenticate 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
search_term="@chipotletweets AND sick"

#get previous tweet record
history=pd.read_csv("#filepath+twitter_history.csv")

#empty list to temp store values
tweet_=[]
id_str_=[]
date_=[]
location_=[]
twitter_id_=[]

#get tweets from API search_term, one day at a time
count1=0
while count1<=10:
    end_date=(datetime.now().date()-timedelta(days=count1))
    start_date=str(end_date-timedelta(days=1))
    end_date=str(end_date)
    print(start_date, end_date)
    search_results = api.search(q=search_term, count=1000, since=start_date, until=end_date,result_type='recent', wait_on_rate_limit=True, lang="en")

    #go through search results and process    
    count2=0
    for x in search_results:
        #test if already tweet already included in list.  this is due to overlapping search queries by date
        if id_str_.count(x._json.get("id_str"))==0:
            tweet_.append(x._json.get("text"))
            id_str_.append(x._json.get("id_str"))
            date_.append(x._json.get("created_at"))
            location_.append(x._json.get("user").get("location"))
            twitter_id_.append(x._json.get("user").get("id"))
            count2+=1
            print(count2)
        else:
            count2+=1            
    count1+=1

dataframe=pd.DataFrame({'message':tweet_, 'message_id':id_str_, 'date':date_, 'location':location_, 'user_id':twitter_id_})

#append into historical record if not already there
count3=0
while count3<len(dataframe['message_id']):
    test=dataframe['message_id'][count3]
    test_list=history['message_id'].tolist()
    if  test_list.count(test)==0:
        history=history.append(dataframe.iloc[count3,:], ignore_index=True) 
        count3+=1        
    else:
        count3+=1

dataframe.to_csv("#filepath+twitter_history.csv", index=False)
