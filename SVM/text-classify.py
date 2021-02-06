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
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score

class Prediction:
    def __init__(self, p):
        self.path = p

    def predict():
        # f=open("temp-predict.txt", "w")
        predictions = []
        svm = []
        nb = []
        sa-score = []

        #Set Random seed
        np.random.seed(500)

        np.set_printoptions(threshold=np.inf)

        # Add the Data using pandas
        # Corpus = pd.read_csv(r"data2.csv",encoding='latin-1')
        Corpus = pd.read_csv(self.path, encoding='latin-1',na_filter=False)
        Train = pd.read_csv(r'train50.csv', encoding='latin-1', na_filter=False)

        # for entry in Corpus['text_final']:
        #     print(entry)

        # Step - 1: Data Pre-processing - This will help in getting better results through the classification algorithms

        # Step - 1a : Remove blank rows if any.
        Corpus['text_final'].dropna(inplace=True)

        # Step - 1b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
        Corpus['text_final'] = [entry.lower() for entry in Corpus['text_final']]

        # Step - 1c : Tokenization : In this each entry in the corpus will be broken into set of words
        Corpus['text_final']= [word_tokenize(entry) for entry in Corpus['text_final']]

        # Step - 1d : Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.

        # WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV


        for index,entry in enumerate(Corpus['text_final']):
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
        Train_X = Train['text_final']
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

        # Step - 5: Now we can run different algorithms to classify out data check for accuracy

        # Classifier - Algorithm - SVM
        # fit the training dataset on the classifier
        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        SVM.fit(Train_X_Tfidf,Train_Y)

        # predict the labels on validation dataset
        predictions_SVM = SVM.predict(Test_X_Tfidf) 
        for ent in predictions_SVM:
            svm.append(ent)
            # fsvm.write(str(ent) + '\n')
            
        # # fit the training dataset on the NB classifier
        Naive = naive_bayes.MultinomialNB()
        Naive.fit(Train_X_Tfidf,Train_Y)

        # # predict the labels on validation dataset
        predictions_NB = Naive.predict(Test_X_Tfidf)

        from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia

        hal = sia()
        for sent in Corpus['text_final']:
            sentence = " ".join(sent)

            ps = hal.polarity_scores(sentence)
            # f.write(str(ps['compound']) + "\n")
            
            score = ps['compound']
            
            if score < 0:
                sa.append("-1")
            elif score == 0:
                sa.append("0")
            else:
                sa.append("1")
            # break
            

        # f.write(str(predictions_SVM))
        # f.write("\n\n\n\n\n")

        # f.write(str(predictions_NB))
        for ent in predictions_NB:
            # fnb.write(str(ent) + '\n')
            nb.append(ent)            
        
        # f.close()
        # f2.close()
        # fsvm.close()
        # fnb.close()

        # f.write(str(predictions_SVM))

        predictions.append(Corpus["date"])
        predicions.append(svm)
        predictions.append(nb)
        predictions.append(sa)

        predictionsOut = zip(predictions)

        # monthly = "month\tsvm\tnb\tsa\n"
        output = "date\tsvm\tnb\tsa\n"
        for ent in predictionsOut:
            output += ent[0] + "\t" + str(ent[1]) + "\t" + str(ent[2]) + "\t" + str(ent[3]) + "\n"

        tempFile = open("temp-predictions.tsv", 'w')
        tempFile.write(outputStr)

        # Use accuracy_score function to get the accuracy
        # print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)