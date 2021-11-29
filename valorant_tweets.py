import os
import tweepy as tw
import pandas as pd
import time
import datetime

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
# You can use your keys unfortunately I can't share it

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def show_tweets(search_word):
    start = time.time()
    tweets = tw.Cursor(api.search,
                  q=search_word+' -filter:retweets', tweet_mode="extended",
                  lang="en").items(20)


    for tweet in tweets:
        print(f'Tweets is :    {tweet.full_text}', tweet.created_at)
        print ('---')

    end = time.time()
    print(f"It took {round(end - start, 2)} Seconds to get tweets")

show_tweets('sova')
df = pd.DataFrame(columns=['tweet', 'date', 'Agent', 'Role'])

def get_tweets(search_word, role):
    global df
    start = time.time()

    tweets = tw.Cursor(api.search,
                  q=search_word+' -filter:retweets', tweet_mode="extended",
                  lang="en").items(1000)

    users_locs = [[tweet.full_text,tweet.created_at, search_word, role] for tweet in tweets]
    tweets = pd.DataFrame(data=users_locs, 
                        columns=['tweet','date', 'Agent', 'Role'])
    tweets['Agent'] = search_word.capitalize()
    tweets['Role'] = role
    df = df.append(tweets)

    end = time.time()
    print(f"It took {round(end - start, 2)} Seconds to get tweets")

df.head()

#I had to get the data o every agent separately as the maximum tweets while using Twitter APII
get_tweets('brimstone', 'Controller')
get_tweets('phoenix', 'Duelist')
get_tweets('sage', 'Sentinel')
get_tweets('sova', 'Initiator')
get_tweets('viper', 'Controller')
get_tweets('cypher', 'Sentinel')
get_tweets('reyna', 'Duelist')
get_tweets('killjoy', 'Sentinel')
get_tweets('breach', 'Initiator')
get_tweets('omen', 'Controller')
get_tweets('jett', 'Duelist')
get_tweets('raze', 'Duelist')
get_tweets('skye', 'Initiator')
get_tweets('yoru', 'Duelist')
get_tweets('astra', 'Controller')
get_tweets('kayo', 'Initiator')

df.shape
df['Agent'].value_counts()

df.to_csv('valorant_tweets.csv', index=False)