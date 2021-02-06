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
indexFile = open("indexPD.txt", 'r') 
dataFile = open("data-PD-Article.tsv", 'w')

dataFile.write('article\tdate\n')

# indexFile = open("/Users/ryanhebert/Desktop/Data/Data/CNN/indexTW.txt", 'r') 

lines = indexFile.readlines()
counter = 1
failed = 0

for line in lines:
    line = line.strip()
    try:
        article = Article(line)
        article.download()
        article.parse()
        text = article.text
        
        r = requests.get(line).text
        soup = BeautifulSoup(r, "lxml")
        pretty = soup.prettify()
        
        x = re.compile(r"(\w{3,10} \d{2}, \d{4})")
        dt = x.search(pretty)
        
        tweet = re.compile('detected that JavaScript|Daily, China on Facebook|People\'s Daily, Chinan|Facebookn')
        if tweet.search(text) is None and dt is not None: 
            # text = text.strip('\r\n\t')
            text = text.replace('\n', '')
            text = text.replace('\t', '')
            text = text.replace('\r', '')
            # print(text)
            date = dt.group(1)
            print(date)
            dataFile.write(text + " \t" + date + '\n')
            dataFile.flush()
            
            counter = counter + 1
        else:
            failed = failed + 1
            print("Not An Article: " + line)
    except:
        pass
    
    print(str(counter + failed) + '/' + str(len(lines)))
    
print('found: ' + str(counter))
print('failed: ' + str(failed))
# dataFile.close()
indexFile.close()