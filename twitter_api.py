import tweepy
import linecache
import pandas as pd
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer

# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = linecache.getline('twitter_api.md',42)
consumer_secret = linecache.getline('twitter_api.md',46) #'HIDDEN'
access_token =    linecache.getline('twitter_api.md',55) #'HIDDEN'
access_secret =   linecache.getline('twitter_api.md',58) # 'HIDDEN'

auth = OAuthHandler(consumer_key[:-1], consumer_secret[:-1])
auth.set_access_token(access_token[:-1], access_secret[:-1])

api = tweepy.API(auth, wait_on_rate_limit=True ,  wait_on_rate_limit_notify=True) 


#tweet = api.get_status(id_of_tweet)
#print(tweet.text)


# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
df_1 = pd.read_csv('twitter-archive-enhanced.csv')

tweet_ids = df_1.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)