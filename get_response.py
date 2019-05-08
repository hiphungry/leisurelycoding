# -*- coding: utf-8 -*-
"""
Created on Tue May 15 16:12:44 2018

@author: me
"""
#function to get appropriate response from Dr. Evil quote file based on latest tweet

def response(tweet, tweet_ID):
    import pandas
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
        
    #import scripts and drevil responses
    sentences=pandas.read_pickle("filepath/drevil_input")
    responses_used=pandas.read_csv("filepath/responses_used.csv")
    #feature development using Tfid
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences['context'])

    #clustering
    model = KMeans(n_clusters=100, init='k-means++', max_iter=100, n_init=1)
    labels=model.fit_predict(X)
    labels=labels.tolist()
    sentences['labels']=labels

    #predict cluster based on input tweet
    test=[tweet]
    test=vectorizer.transform(test)
    response_cat=(model.predict(test)[0])

    #get all appropriate drevil response
    responses=sentences.loc[sentences['labels'] == response_cat]
    
    #get record of previous items tweeted responsed to and quotes tweeted 
    responses_used=pandas.read_csv("filepath/responses_used.csv")    

    #check if already responded to tweet
    if int(tweet_ID)==responses_used['tweet_ID'][0]:
        return('False',"")
    else:
        previoustweet=True
        count=0
        #choose response and compare against previous
        while previoustweet:
            chosen=responses.sample(n=1,axis=0)
            chosenindex=[chosen.index.values[0]]
            print(chosenindex[0])
            testvalue=responses_used['responses_used'][:10].isin(chosenindex)
            if sum(testvalue)==0:
                previoustweet=False
            else:
                previoustweet=True
            if count==10:
                previoustweet=False
            count+=1

    #record used response
        responses_used.loc[-1] = [chosenindex[0], int(tweet_ID)]  # adding a row
        responses_used.index = responses_used.index + 1  # shifting index
        responses_used = responses_used.sort_index()
        responses_used.to_csv("filepath/responses_used.csv", index=False)

    #return quote
        response=chosen['drevil']
        joinresponse=' '.join(response[chosenindex[0]][2:])
        return('True', joinresponse)