import re, os 
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from textclassify import Prediction
from nltk.stem import PorterStemmer
from visual import Visual

class Process:
    def __init__(self, pth, sf, sw, stem):
        self.path = pth
        self.singleFile = sf
        self.sw = sw
        self.stem = stem

    def cleanSW(self, words):
        sw = []
        swords = open("sw.txt", 'r')
        swords = swords.read()
        for word in swords.split():
            word =  word.strip()
            sw.append(word)
        out = [word for word in words.split() if not word.lower() in sw]
        output = " ".join(out)
        return output
    
    def cleanPunct(self, words):
        words = re.sub(r'[^\x00-\x7f]',r'', words) # removes garbage chars 
        return re.sub(r'[^\w\s]', '', words) # removes punctuation 

    def cleanNums(self, words):
        return re.sub(r'\d+', 'num', words)


    def stemWords(self, words):
        porter = PorterStemmer()
        out = ""
        for word in words.split():
            out = out + porter.stem(word) + ' '
        return out

    def cleanContents(self, content):
        if self.sw:
            content = self.cleanSW(content)
        if self.stem:
            content = self.stemWords(content)
        
        content = self.cleanNums(content)
        content = self.cleanPunct(content.lower())
        
        return content
        
    def preProcess(self):
        outputStr = "text,date\n"
        if self.singleFile:
            content = open(self.path, "r", encoding = "latin-1")
            link = content.readline()
            date = content.readline()
            article = content.read().replace('\n', '')
            article = self.cleanContents(article, self.sw)

            outputStr += article + "," + date
        else:
            for f in os.listdir(self.path):
                content = open(self.path + f, "r", encoding = "latin-1")
                link= content.readline()
                date=content.readline()
                article = content.read().replace('\n', '')

                article = self.cleanContents(article)

                outputStr += article + "," + date 

        tempFile = open("temp-data.csv", 'w')
        tempFile.write(outputStr)
        tempFile.close()
        
    def process(self):
        predictor = Prediction("temp-data.csv")
        predictor.predict()
        
    def visualize(self, o):
        if o == 1:
            os.system("bokeh serve visual.py")
        elif o == 2:
            os.system("bokeh serve visual2.py")

path = os.path.dirname(os.path.abspath(__file__)) + '/separated'
test = Process(r'/Users/ryanhebert/Desktop/Research/Data/CNN/TweetsHK/', False, True, True)
test.preProcess()
test.process()
test.visualize(1)