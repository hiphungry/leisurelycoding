# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:08:38 2018

@author: me
"""
#confirms address with orange county tax departemnt

import urllib
from bs4 import BeautifulSoup
import pandas
import time

#get zipcode for file names add '_street'
zipcode=pandas.read_csv("C:/Users/me/Documents/Python Scripts/ca45_zip.csv")

#get zip_street file.  zip_street file contains list of streets and numbers for each zip code.  source: melissa.com
x=#zipcode: iterate through list or just one
x=str(x)
zip_street=x+'_street.csv'
data=pandas.read_csv("#filepath"+zip_street)

count=0
length=len(data['street'])
while count<length:
    count_negative=0
    #builds addresses
    y=data['street'][count]
    street=y.split('Name=')[1]
    street=street.replace('+','%20')

    low_it=int(data['nlow'][count])
    low=low_it
    high=int(data['nhigh'][count])
    count2=0
    address=[]
    while low_it<=(high):
        #build address
        test_number=(str(data['odd_even'][count]))
        if(len(test_number)==3):
            low_it=low+count2
        else:
            low_it=low+count2*2
        url="http://tax.ocgov.com/tcweb/search_addr.asp?streetname="+str(low_it)+"%20"+street+"&t_city="

        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers={'User-Agent': user_agent}
            req=urllib.request.Request(url, headers=headers)
            response=urllib.request.urlopen(req)
#            response=urllib.request.urlopen(url, headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
        except urllib.error.URLError as e:
            print(e)
            time.sleep(30)
            response.close()
        else:
            html=(response.read())
            response.close()
#        print(html)

        #html_parse=html.page_source
            soup=BeautifulSoup(html, "html.parser")
            container=soup.find_all("td", attrs={"colspan":"7", "class":"contentbold3", "align":"center"})
            if(len(container)==0):
                count_negative=0
                address.append(str(low_it)+'+'+street.replace('%20','+'))
                print(str(low_it)+'+'+street.replace('%20','+'))
                print('add address')
#        print(container)
            else:
                container=str(container[0])
                if ('No address was found that matches your criteria.' in container):
                    count_negative+=1
                    #                print(str(low_it)+'+'+street.replace('%20','+'))
                    #                print('not an address')
                    if count_negative>=100:
                        low_it=high+1
#        print(low_it, high)
            count2+=1
    data_df={'address':address}#, 'street':street_name, 'url':link}
    df = pandas.DataFrame(data=data_df)
    file_path="#filepath"+x+"/address_confirm"+x+'+'+str(street.replace('%20', '+'))+"_confirmed.csv"
    df.to_csv(file_path, index=False)
    print('write file', str(street))
    print(count)
    count+=1            