from typing import Text
import pymongo 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from sqlalchemy import create_engine
import logging
import re

s  = SentimentIntensityAnalyzer()

# Establishing a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

#Establishing a connection to the Postgresdb server
pg = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitter', echo=True)
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
    );
''')

# Selecting the database you want to use withing the MongoDB server
db = client.twitter
time.sleep(10)  # seconds

docs = db.tweets.find()

for tweet in docs:
    tweet = tweet['text'].lower()
    tweet = re.sub(r'&amp;','and ',tweet) 
    tweet_sent = s.polarity_scores(tweet)
    tweet_sent = tweet_sent['compound']
    text = tweet
    score = tweet_sent
    query = "INSERT INTO tweets VALUES (%s, %s);"
    pg.execute(query, (text, score))
    
    
   

