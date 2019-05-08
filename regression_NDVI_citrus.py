# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 08:27:56 2018

@author: me
"""
import pandas
import statsmodels.api as sm
import numpy as np

#import consolidated data file
data = pandas.read_csv("C:/Users/me/Documents/Python Scripts/citrus/historical_citrus3_no2012.csv", engine='python')
z=data['Yield_Per_Acre']

#regression
X=np.column_stack((data['diff_wind'], data['diff_precip'], data['diff_storms'], data['DeSoto'], data['Hardee'], data['Hendry'], data['Highlands'], data['Polk'], data['StLucie'], data['mDeSoto_NDVI'], data['mHardee_NDVI'], data['mHendry_NDVI'], data['mHighlands_NDVI'], data['mPolk_NDVI'], data['mStLucie_NDVI']))#data['DeSoto_NDVI'], data['Hardee_NDVI'], data['Hendry_NDVI'], data['Highlands_NDVI'], data['Polk_NDVI'], data['StLucie_NDVI']))
model=sm.OLS(z,X)
results=model.fit()
print(results.summary())

forecast=results.predict(X)

#calculate in-sample MAPE
length=len(z)
count=0
mape_total=0
while count<length:
    mape=(abs(z[count]-forecast[count])/z[count])
    print (mape, forecast[count])
    mape_total=mape_total+mape
    count+=1
    
print ('average: '+str(mape_total/length))
