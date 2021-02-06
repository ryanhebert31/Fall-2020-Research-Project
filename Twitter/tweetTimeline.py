#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:15:14 2020

@author: jorgesilveyra
"""



import tweepy 
import json, re, twint
import datetime as dt

CONSUMER_KEY        = 'qyUVAYpSOGgYyK067Y6QYUtbF'
CONSUMER_KEY_SECRET = 'hueDHiV1mmOgtvUhmgDKvzebCIlq3Uk0Iw6fWMQEmDtHRqp9Xr'
ACCESS_TOKEN        = '1250462170825007104-CHA1CqaGeIA17llWT7ZVg9f4eyLNWB'
ACCESS_TOKEN_SECRET = 'UYtpql2kVTZGFG6YUPx73diJdpPwRMdCCDsOgX8fCJrn2'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
tweets = 0
hk = 0
tw = 0
links = 0

search = api.user_timeline(screen_name = 'globaltimesnews', count = 200, tweet_mode="extended") 

F_NAME = 'globalTimesTimeline.json'
index = open("index.txt", 'w')

last = ""

c = twint.Config()
c.Username = 'globaltimesnews'
c.limit = 10
c.Store_csv = True
c.Output = 'none'

with open(F_NAME,'w') as f_out:
    for status in search:
        print(status.id)

        last = status.id
        for url in status.entities['urls']:
            x = re.compile('twitter.com')
            if x.search(url['expanded_url']) is None:
                index.write(url['expanded_url'])
                index.write('\n')
                index.flush()
                links = links + 1
                if t is True:
                    indexT.write(url['expanded_url'])
                    indexT.write('\n')
                    indexT.flush()
                    tw = tw + 1
                if h is True:
                    indexHK.write(url['expanded_url'])
                    indexHK.write('\n')
                    indexHK.flush()
                    hk = hk + 1
        json.dump(status._json, f_out,indent=4)
        f_out.write('\n')
        tweets = tweets + 1
        
    for i in range(15): 
        search = api.user_timeline(screen_name = 'globaltimesnews', count = 200, max_id = 1303645833057845249) # 1303645833057845249 test with this
        for status in search:
        # for status in tp.Cursor(api.user_timeline(screen_name = 'globaltimesnews', count = 200, max_id = 1303645833057845249, tweet_mode='extended')).items()
            # if last == status.id:
            #     print('Duplicate')
            #     break
            print(status.id)
            h = False
            t = False
            hkSearch = re.compile(r'\#?[Hh]ong\s?[Kk]ong')
            if hkSearch.search(status.text) is not None:
                h = True
            tSearch = re.compile(r'\#?[Tt]aiwan')
            if tSearch.search(status.text) is not None:
                t = True
            last = status.id
            # urlSearch = re.compile(r'https://t.co/') #TODO: Start here 
            
            for url in status.entities['urls']:
                x = re.compile('twitter.com')
                if x.search(url['expanded_url']) is None:
                    index.write(url['expanded_url'])
                    index.write('\n')
                    index.flush()
                    links = links + 1
                    if t is True:
                        indexT.write(url['expanded_url'])
                        indexT.write('\n')
                        indexT.flush()
                        tw = tw + 1
                    if h is True:
                        indexHK.write(url['expanded_url'])
                        indexHK.write('\n')
                        indexHK.flush()
                        hk = hk + 1
            json.dump(status._json, f_out,indent=4)
            f_out.write('\n')
            tweets = tweets + 1
            
            
print('\n--------------------------------\n' + str(tweets) + " tweets discovered.")

print(str(links) + ' links pulled.')
print(str(hk) + ' contain the query \'Hong Kong\'')
print(str(tw) + ' contain the query \'Taiwan\'')

# index.close()
# indexT.close()
# indexHK.close()
# log.write(str(dt.datetime.now()))
# log.write(str(last))
# log.close()