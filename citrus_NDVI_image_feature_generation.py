# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:47:47 2018

@author: me
"""
#iterates through weekly satellite image (NDVI) files from USDA for six highest citrus producing counties in florida and outputs features
from scipy import misc
import glob

#counties for analysis
counties=['Highlands', 'Polk', 'StLucie', 'Hardee', 'Hendry', 'DeSoto']
c_count=0

#week
w_count=1
weeks=[]
while w_count<53:
    if w_count<10:
        w_str='_0'+str(w_count)+'_'
    else:
        w_str='_'+str(w_count)+'_'        
    weeks.append(w_str)
    w_count+=1

#counties loop
counties=['DeSoto', 'Hardee', 'Hendry', 'Highlands', 'Polk', 'StLucie']
w_count=0
count=2012

year=[]
max_img=[]
county=[]

while count<2013:
    for x in counties:
        #define the directory
        f_name='filepath'+str(count)+'_'+x+'/NDVI_'#+weeks[w_count]

        f_names=[]
        images=[]
        for name in glob.glob(f_name+'*'):
                f_names.append(name)
                img=misc.imread(name) #read image
                #convert image to value
                img=img[::2,::2] 
                X=(img/255.0).reshape(-1) 
                images.append(sum(X))
        length2=len(f_names)
        while length2<53:
            f_names.append('')
            images.append(0)
            length2=len(f_names)
        
        w2_count=0
        while w2_count<52:
            if weeks[w2_count] in f_names[w2_count]: #search for string _01_
                w2_count+=1
            else:
                f_names.insert(w2_count, '')
                images.insert(w2_count, 0)
                w2_count+=1    
        length=len(f_names)-1
        while length>51:
            f_names.pop()
            images.pop()
            length=len(f_names)-1
        year.append(count)
        max_img.append(max(images))
        county.append(x)
        print (count, x, max(images), sum(images)/52, max(images)/(sum(images)/52), len(images), max(images[35:45])/(sum(images[35:45])/len(images[35:45])))
    count+=1

