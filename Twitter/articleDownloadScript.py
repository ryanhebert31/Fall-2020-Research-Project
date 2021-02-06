#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:39:13 2020

@author: ryanhebert

"""

from bs4 import BeautifulSoup
import re, requests
from newspaper import Article
import json

# indexFile = open("/Users/ryanhebert/Desktop/Data/Data/PD/indexHK.txt", 'r') 
indexFile = open("/Users/ryanhebert/Desktop/Research/Twitter/indexHK.txt", 'r') 

# indexFile = open("/Users/ryanhebert/Desktop/Data/Data/CNN/indexTW.txt", 'r') 

lines = indexFile.readlines()
counter = 1
  
for line in lines:
    line = line.strip()
    try:
        article = Article(line)
        article.download()
        article.parse()
        
        tweet = re.compile('detected that JavaScript|Daily, China on Facebook|People\'s Daily, Chinan|Facebookn')
        if tweet.search(article.text) is None:  
            
            f = open('/Users/ryanhebert/Desktop/Research/Twitter/HK/file'+ str(counter) +'.txt', 'w')
            f2 = open('/Users/ryanhebert/Desktop/Research/Twitter/HK/file'+ str(counter) +'c.txt', 'w')

            f.write(line)
            f.write('\n')
            f2.write(line)
            f2.write('\n')
       
            f2.write(article.title)
            f2.write('n')
            f2.write(article.text)
            
            r = requests.get(line).text
            soup = BeautifulSoup(r, "lxml")
            pretty = soup.prettify()
            f.write(pretty)
        
            f.close()
            f2.close()
            counter = counter + 1
        else:
            print("Tweet or FaceBook: " + line)
    except:
        pass
print(counter)
indexFile.close()