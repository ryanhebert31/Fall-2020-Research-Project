#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:05:16 2020

@author: ryanhebert
"""

import json, re

def checkForHK(tweet):
    x = re.compile(r'\#?[Hh]ong\s?[Kk]ong')
    # x=re.compile(r'\#?[Cc]hina')
    # print('found')
    if x.search(tweet) is not None:
        return True
    return False

def checkForTW(tweet):
    x = re.compile(r'\#?[Tt]aiwan')
    if x.search(tweet) is not None:
        return True
    return False

def tryGetLinks(tweet):
    
    x = re.compile(r'(https://t\.co/[a-zA-Z0-9]*)')#//t\.co/(\w{1, 11})') #https://t.co/13a5D02b5b
    srch = x.findall(tweet) 
    if srch is not None:
    
        return srch
    
    return []


with open('peoplesDaily.json', 'r') as js:
    index = open('indexPD.txt', 'w')
    # indexTW = open('indexTW.txt', 'w')
    
    count = 1

    
    for line in js.readlines():
        dicto = json.loads(line)
        
        tweet = dicto['tweet']
        # print(tweet)
        date = dicto['date']
        tweetUrl = dicto['link']
        
        urls = tryGetLinks(tweet)
        
        two = False 
        for url in urls:
            # print(url)
            index.write(url + '\n')
        
        twt = open("Tweets/file" + str(count) +".txt", 'w')
        twt.write(date)
        twt.write('\n')
        twt.write(tweet)
        twt.close()
            
        count = count + 1
        # if count == 5:
        #     break
            
    # indexHK.close()
    # indexTW.close()
    print(str(count) + ' tweets analyzed.')
    
            

