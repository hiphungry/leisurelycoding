# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:53:04 2018

@author: me
"""
#samples addresses in city, then looks up address in zillow and scrapes information from it, then records summary information of sample on per sq ft basis: zestimate, recently sold, for sale

import pandas
import math
from bs4 import BeautifulSoup
import urllib
import time
import random
import datetime
import numpy as np

file_path="#list of addresses+data_all.csv"

history_data=pandas.read_csv("#historical record of property values + history6.csv")
data=pandas.read_csv(file_path)
rsample = random.sample(range(0,22186), 2000)
count=0

t_hv_sqft=[]
t_fs_sqft=[]
t_fs_days=[]
t_fr_sqft=[]
t_rs_sqft=[]

pf_l=[]
pf_price_l=[]

status=[]
amount=[]

for x in rsample:
    url="https://www.zillow.com/homes/for_sale/Irvine-CA/_type/"+str(data['zpid'][x])+"_zpid/"
    time.sleep(1.5)
#    zpid.append(data['zpid'][count])
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
#        print(html)
        response.close()
#        print(html)

        #html_parse=html.page_source
        soup=BeautifulSoup(html, "html.parser")
        container=soup.find_all("meta", attrs={"property":"zillow_fb:description"})#,
        container2=str(soup.find_all("meta", attrs={"name":"description"}))
        container3=soup.find_all("div", attrs={"class":"pre-foreclosure-auction"}) 


        if (math.isnan(data['buildsize'][x])):
            print('build is nan')
        else:
            if len(container)==0:
                count+=1                
            elif ('pre-foreclosure-auction' in str(container3)):
                container4=soup.find_all("div", attrs={"class":"zestimate"})#("meta")#, 
                container4=str(container4[0]).split('>$')
                container4=container4[1].split('<')
                amount=(container4[0].replace(',',''))
                pf_price_l.append(int(amount))
                pf_l.append(1)
                print(count, 'pre-foreclosure: ', amount)
                count+=1
            elif (('Home Value' in str(container))and('$' in str(container))):
                container=str(container[0]).split('.')
                container=container[0].split(' ')
                amount.append(container[4]) #amount
                status.append(container[3].replace(':','')) #zest'imate
#                print(x, container[4], container[3], data['zpid'][x], data['buildsize'][x])
                zestimate=(container[4].replace(',','').replace('$',''))
                test='5'
                try:
                    int(zestimate)
                except:
                    print('int failed')
                    count+=1
                else:    
                    zestimate=int(zestimate)
                    z_sqft=zestimate/int(data['buildsize'][x])
                    print(count, 'hv: ', z_sqft, 'build type: ', data['type'][x])
                    t_hv_sqft.append(z_sqft)
                    count+=1                    
            elif ('For sale:' in str(container)): #recently sold, sale, rent
                container=str(container[0]).split('.')
                container=container[0].split(' ')
                amount.append(container[3]) #amount
                status.append(container[2].replace(':','')) #sale or rent or sold
#                print(x, container[3], container[2], data['zpid'][x], data['buildsize'][x])
                price=int(container[3].replace(',','').replace('$',''))
                fs_sqft=price/int(data['buildsize'][x])
                print(count, 'fs: ',fs_sqft, 'build type: ', data['type'][x])
                t_fs_sqft.append(fs_sqft)
                count+=1
            elif ('Recently sold:' in str(container)):
                container=str(container[0]).split('.')
                container=container[0].split(' ')
                amount.append(container[3]) #amount
                status.append(container[2].replace(':','')) #sale or rent or sold
                price=int(container[3].replace(',','').replace('$',''))
                rs_sqft=price/int(data['buildsize'][x])
                print(count, 'rs: ', rs_sqft, 'build type: ', data['type'][x])
                t_rs_sqft.append(rs_sqft)
                count+=1            

            if ('listed for-sale' in container2): #for sale
                container3=(soup.find_all("div", attrs={"class":"fact-value"}))
                print(container3)
                if (len(container3)<1):
                    pf_l.append(1)
                    count+=1
                else:
                    container3=(str(container3[6]).split('>')[1])
                    if ('Days' in container3):
                        days=int(container3.split(' Days')[0])
    #                days_on_market+=container3
                    elif ('No Data' in container3):
                        days=float('nan')
                    elif ('Less than 1' in container3):
                        days=float(1.0)
                    elif ('Day' in container3):
                        days=int(container3.split(' Day')[0])
                    elif ('sqft' in container3):
                        days=float('nan')
                    else:
                        days=int(container3.split('<')[0])
                    t_fs_days.append(days)
                    print('days on market: ', days)#days on market
                    count+=1  
#                count_forsale+=1

names=['date', 'hv_sqft', 'hv_sqft_stdv', 'hv_cnt', 'fs_sqft', 'fs_sqft_stdv', 'fs_days', 'fs_days_stdv', 'fs_cnt', 'rs_sqft', 'rs_sqft_stdv', 'rs_cnt']
#final append values
today = datetime.date.today()

#remove min/ max from each sample...
if (len(t_hv_sqft)>5):
    t_hv_sqft.remove(min(t_hv_sqft))
    t_hv_sqft.remove(min(t_hv_sqft))
    t_hv_sqft.remove(max(t_hv_sqft))
    t_hv_sqft.remove(max(t_hv_sqft))
    t_hv_sqft.remove(max(t_hv_sqft))
if (len(t_fs_sqft)>5):
    t_fs_sqft.remove(min(t_fs_sqft))
    t_fs_sqft.remove(max(t_fs_sqft))
if (len(t_fr_sqft)>5):
    t_fr_sqft.remove(min(t_fr_sqft))
    t_fr_sqft.remove(max(t_fr_sqft))
if (len(t_rs_sqft)>5):
    t_rs_sqft.remove(min(t_rs_sqft))
    t_rs_sqft.remove(max(t_rs_sqft))

#'home value'
avg_hv_sqft=np.mean(t_hv_sqft)
stdv_hv_sqft=np.std(t_hv_sqft)
hv=len(t_hv_sqft)
#'for sale'
avg_fs_sqft=np.mean(t_fs_sqft)
stdv_fs_sqft=np.std(t_fs_sqft)
avg_fs_days=np.mean(t_fs_days)
stdv_fs_days=np.std(t_fs_days)
fs=len(t_fs_sqft)
#'for rent'
avg_fr_sqft=np.mean(t_fr_sqft)
stdv_fr_sqft=np.std(t_fr_sqft)
fr=len(t_fr_sqft)
#'recently sold
avg_rs_sqft=np.mean(t_rs_sqft)
stdv_rs_sqft=np.std(t_rs_sqft)
rs=len(t_rs_sqft)
#'pre-foreclosure'
pf=len(pf_l)
avg_pf_p=np.mean(pf_price_l)
#print(t_fs_days)


add=[today, avg_hv_sqft, stdv_hv_sqft, hv, avg_fs_sqft, stdv_fs_sqft, avg_fs_days, stdv_fs_days, fs, avg_fr_sqft, stdv_fr_sqft, fr,avg_rs_sqft, stdv_rs_sqft, rs, pf, avg_pf_p]

history_data.loc[-1] = add  # adding a row
history_data.index = history_data.index + 1  # shifting index
history_data = history_data.sort_index()  

history_data.to_csv("#historical record of property values + history6.csv", index=False)