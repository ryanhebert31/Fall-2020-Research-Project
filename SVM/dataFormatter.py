#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:59:09 2020

@author: ryanhebert
"""

import csv, os, re
import pandas as pd


from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia

hal = sia()

# test = ["this is awesome", 'this is awful']

# for sentence in test:
#     # print(sentence)
#     ps = hal.polarity_scores(sentence)
#     print(ps['compound'])
#     # for k in sorted(ps):
#     #     print('\t{}: {:>1.4}'.format(k, ps[k]), end='  ')
#     print()



outputStr = "article\tdate\n"
output = open("data-PD-Tweets.tsv", "w")

# fnum = 1
# while True:
    
#     try:
       
#         html = open("HK/file" + str(fnum) + ".txt", "r")
#         body = open("HK/file" + str(fnum) + "c.txt", "r")
        
#         x = re.compile(r"Published\: (\d\d\d\d\/\d{1,2}/\d{1,2})")
        
#         body.readline()
#         body = body.read().strip()
#         body = ' '.join(body.split())
#         # print(body)
        
#         html = html.read()
#         # print(html)
#         dt = x.search(html)
        
#         if dt is not None:
#             date = dt.group(1)
            
#             row = body + " \t"+ date + "\n"
#             # print(row)
#             outputStr = outputStr + row
            
#         fnum = fnum + 1

            
#     except:
#         break



# fnum = 1
# while True:
#     try:
#         content = open("Tweets/file" + str(fnum) + ".txt", "r")
    
#         # link = content.readline()
#         date = content.readline()
#         tweet = content.readlines()
        
#         date = date.strip()
#         twee = tweet[0].strip()
#         # print(link)
#         # print(date)
#         # print(tweet)
        
#         row = twee + " \t"+ date + "\n"
    
#         outputStr += row
        
#         content.close()
        
#         fnum += 1
#     except:
#         print('broken')
#         break
   
    
output.write(outputStr)
output.close()
