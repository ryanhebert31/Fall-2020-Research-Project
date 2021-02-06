#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:34:25 2020

@author: ryanhebert
"""

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
from sklearn import model_selection, naive_bayes, svm  #SVM
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC  # SVC ? 
from ast import literal_eval
import csv, re

class Prediction:
    def __init__(self, path):
        self.path = path

    def predict(self):
        predictions = []
        
        #Set Random seed
        np.random.seed(500)
        np.set_printoptions(threshold=np.inf)

        # Add the Data using pandas
        Corpus = pd.read_csv(self.path, encoding='latin-1', na_filter=False)
        Train = pd.read_csv(r'train50.csv', encoding='latin-1', na_filter=False)

        # Step - 1: Data Pre-processing - This will help in getting better results through the classification algorithms

        # Step - 1a : Remove blank rows if any.
        Corpus['text'].dropna(inplace=True)

        # Step - 1b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
        Corpus['text'] = [entry.lower() for entry in Corpus['text']]

        # Step - 1c : Tokenization : In this each entry in the corpus will be broken into set of words
        Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]

        # Step - 1d : Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.

        # WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV


        for index,entry in enumerate(Corpus['text']):
            # Declaring Empty List to store the words that follow the rules for this step
            Final_words = []
            # Initializing WordNetLemmatizer()
            word_Lemmatized = WordNetLemmatizer()
            # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
            for word, tag in pos_tag(entry):
                # Below condition is to check for Stop words and consider only alphabets
                if word not in stopwords.words('english') and word.isalpha():
                    word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                    Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
            Corpus.loc[index,'text_final2'] = str(Final_words)
            

        # Step - 2: Split the model into Train and Test Data set
        # Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],Corpus['label'],test_size=0.3)
        # print(Train)
        Train_X = Train['text']
        Train_Y = Train['label']
        Test_X = Corpus['text_final2']


        # Step - 3: Label encode the target variable  - This is done to transform Categorical data of string type in the data set into numerical values
        Encoder = LabelEncoder()
        # print(Train_Y)
        Train_Y = Encoder.fit_transform(Train_Y)
        # Test_Y = Encoder.fit_transform(Test_Y)

        # Step - 4: Vectorize the words by using TF-IDF Vectorizer - This is done to find how important a word in document is in comaprison to the corpus
        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(Corpus['text_final2'])

        Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)

        # Step - 5: Now we can run different algorithms to classify out data check for saccuracy

        # Classifier - Algorithm - SVM
        # fit the training dataset on the classifier
        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        SVM.fit(Train_X_Tfidf,Train_Y)

        # predict the labels on validation dataset
        predictions_SVM = SVM.predict(Test_X_Tfidf) 

            
        # # fit the training dataset on the NB classifier
        Naive = naive_bayes.MultinomialNB()
        Naive.fit(Train_X_Tfidf,Train_Y)

        # # predict the labels on validation dataset
        predictions_NB = Naive.predict(Test_X_Tfidf)

        from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
        hal = sia()

    
        predictions = []
        
        yearlyTotal = {}
        monthlyTotal = {}
        yearlySVM = {}
        monthlySVM = {}
        yearlyNB = {}
        monthlyNB = {}
        yearlyPos = {}
        monthlyPos = {}
        yearlyNeg = {}
        monthlyNeg = {}
            
        for i in range(len(Corpus['date'])):
            
            z = predictions_NB[i]
            
            x = predictions_SVM[i]
            
            sent = " ".join(literal_eval(Corpus['text_final2'][i]))
            ps = hal.polarity_scores(sent)
            if ps['compound'] > 0.1:
                sa = 1
            elif ps['compound'] < -0.1:
                sa = -1
            else:
                sa = 0
            date = Corpus['date'][i]
            exp = re.compile(r'(\d\d\d\d)-(\d\d)-\d\d') # numpy changes date format 
            res = exp.search(date)
            if res is not None:
                month = res.group(2)
                year = res.group(1)
                # print(year)
                temp = [month, year, z, x, sa]
                predictions.append(temp)
                
                my = str(month) + "/" + str(year)
                monthlyTotal[my] = monthlyTotal.get(my, 0) + 1
                yearlyTotal[year] = yearlyTotal.get(year, 0) + 1
                # print(my)
                if x == 1:
                    monthlySVM[my] = monthlySVM.get(my, 0) + 1
                    yearlySVM[year] = yearlySVM.get(year, 0) + 1
                if z == 1:
                    monthlyNB[my] = monthlyNB.get(my, 0) + 1
                    yearlyNB[year] = yearlyNB.get(year, 0) + 1
                if sa == 1:
                    monthlyPos[my] = monthlyPos.get(my, 0) + 1
                    yearlyPos[year] = yearlyPos.get(year, 0) + 1
                elif sa == -1:
                    monthlyNeg[my] = monthlyNeg.get(my, 0) + 1
                    yearlyNeg[year] = yearlyNeg.get(year, 0) + 1
            else:
                print("Error: improper or missing date format: " + str(date) + ". Must be in format yyyy-mm-dd.")

        
        with open('predictions.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Month", "Year", "SVM", "NB", "SA"])
            for prediction in predictions:
                writer.writerow(prediction)
        
        
        ###TODO: Sort dictionary by month in order. there may be a better way to store date
        ### or k in the loop. When you open in excel it defaults to the first of the momnth.
        with open('summary-Monthly.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Total", "SVM", "NB", "SVM%", "NB%", "Positive", "Negative", "Neutral", "Rate"])
            for k, v in monthlyTotal.items():
                # print(monthlySVM)
                svmP = monthlySVM.get(k,0) / v
                nbP = monthlyNB.get(k,0) / v
                pos = monthlyPos.get(k,0)
                neg = monthlyNeg.get(k,0)
                neu = v - (pos + neg)
                if neg != 0 and pos != 0:
                    rate = pos/neg
                elif neg == 0:
                    rate = pos
                else:
                    rate = 1 / neg
                writer.writerow([k, v, monthlySVM.get(k,0), monthlyNB.get(k,0), svmP, nbP, pos, neg, neu, rate])
        
        with open('summary-Yearly.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Total", "SVM", "NB", "SVM%", "NB%", "Positive", "Negative", "Neutral", "Rate"])
            for k, v in yearlyTotal.items():
                # print(k)
                # print(monthlySVM)
                svmP = yearlySVM.get(k,0) / v
                nbP = yearlyNB.get(k,0) / v
                pos = yearlyPos.get(k,0)
                neg = yearlyNeg.get(k,0)
                neu = v - (pos + neg)
                if neg != 0 and pos != 0:
                    rate = pos/neg
                elif neg == 0:
                    rate = pos
                else:
                    rate = 1 / neg
                    
                writer.writerow([k, v, yearlySVM.get(k,0), yearlyNB.get(k,0), svmP, nbP, pos, neg, neu, rate])
            
pred = Prediction(r'temp-data.csv')
pred.predict()