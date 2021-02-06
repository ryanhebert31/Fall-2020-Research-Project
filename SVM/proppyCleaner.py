#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:18:31 2020

@author: ryanhebert
"""

# f = open("test.csv", 'r')

# for thing in 

import csv, re

def lemnatize(words):
        sw = []
        swords = open("sw.txt", 'r')
        swords = swords.read()
        
        for word in swords.split():
            word =  word.strip()
            sw.append(word)
            
        from nltk.stem import PorterStemmer
        out = ''
        porter = PorterStemmer()
        
        for word in words.split():
            if word not in sw:    
                out = out + porter.stem(word) + ' ' 
            
        # print(sw)
        return out
    
def cleanPunct(words):
    words = re.sub(r'[^\x00-\x7f]',r'', words) # removes garbage chars 
    return re.sub(r'[^\w\s]', '', words) # removes punctuation 
    
def cleanNums(words):
    return re.sub(r'\d+', 'num', words)



# file = open('text_final.txt', 'r')

# f = 0

# for line in file.readlines():
#     print(f)
#     for word in line.split():
#         print(word.lower())   
#     f += 1










new = open('trainCleaned.tsv', 'w')
outputStr = '1\t2\n'

with open('train3.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        
        text = row[0]
        text = lemnatize(text)
        text = cleanPunct(text)
        text = cleanNums(text)
        
        outputStr = outputStr + text + '\n'
        
        # if count > 1:
        #     break
        # count = count + 1
        # print(row[1])
        # print(row[0],row[1],r,)
new.write(outputStr)
new.close()