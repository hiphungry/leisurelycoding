# -*- coding: utf-8 -*-
#!/usr/bin/env python
#gets latest tweet and calls "response" function to classify tweet using kmeans model based on kmeans cluster analysis of Dr. Evil quotes from Austin Power scripts.  Then tweets quote.

import tweepy
from keys import keys
from get_response import response

#get keys
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

#authenticate 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#get kardashian tweets
statuses=api.user_timeline(id=25365536)
inputs = [s.text for s in statuses]
ids=[s.id_str for s in statuses]
test_tweet=inputs[0]

#call function to generate response
tweet=response(test_tweet, ids[0])
if tweet[0]=='True':
    status = api.update_status(status=tweet[1]) 
else:
    print('nothing tweeted')
