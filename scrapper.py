import requests
import os
import json
import tweepy
import configparser

#  TODO: Currently waiting for elevated access of Twitter API ro be approved, and only write some sketch (eg. only one example user)
#        to test the current functionality. Next need to consider more targeted users and think about how to connect with DynamoDB (eg. for ID Deduplication)
#        Then, need to auto-crawl (eg. use while True?) and consider crawling limits.

def get_api():
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def get_replies(screen_name, tweet, curr_tweet_replies):
    '''Use recursion to get all replies of the original tweet, and all nested replies of each reply'''
    number_of_replies = 50
    tweet_replies = tweepy.Cursor(
        api.search, q='to:' + screen_name, since_id=tweet.id, tweet_mode="extended", lang='en'
    ).items(number_of_replies)
    for reply_tweet in tweet_replies:
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (reply_tweet.in_reply_to_status_id_str == tweet.id_str):
                curr_tweet_replies.append(reply_tweet.text)
                try:
                    reply_tweet_user_name = reply_tweet.user.screen_name
                    for reply_to_reply in get_replies(reply_tweet_user_name, reply_tweet, curr_tweet_replies):
                        pass
                except Exception:
                    pass
    return curr_tweet_replies

def get_tweets(api, screen_name):
    all_tweets_replies = []
    number_of_tweets = 200
    user_tweets = tweepy.Cursor(
        api.user_timeline, screen_name=screen_name, tweet_mode="extended"
    ).items(number_of_tweets)
    for tweet in user_tweets:
        curr_tweet_replies = []
        all_tweets_replies.append(get_replies(screen_name, tweet, curr_tweet_replies))
    return all_tweets_replies


if __name__ == "__main__":
    api = get_api()
    screen_name = "mikepompeo"
    all_tweets_replies = get_tweets(api, screen_name)
    for curr_tweet_replies in all_tweets_replies:
        print(curr_tweet_replies)
        print('\n')
