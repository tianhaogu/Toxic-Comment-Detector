import requests
import os
import json
import tweepy
import configparser
from scorer import *

NUM_PER_USER = 500
NUM_PER_TWEET = 300
NUM_PER_REPLY = 100
USERS = ["william_tianhao", "mikepompeo", "KDTrey5", "SpeakerPelosi", "TeamPelosi", "billieeilish",
         "KingJames", "willsmith", "KimKardashian", "BarackObama", "JoeBiden", "AnneeJHathaway"]#, 
         #"CNN", "FoxNews", "nytimes"]

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

def process_text(text):
    """Remove the @<username> part of the reply."""
    if text.startswith('@'):
        text_ = text.split()
        new_text = " ".join(text_[1:])
        return new_text
    return text

def get_tweet_replies(api, replied_tweet_, all_tweets_replies_):
    """Recursive function to get all nested replies to the first layer of replies of the current user."""
    curr_replied_user = replied_tweet_.user.screen_name
    replied_replied_tweets = tweepy.Cursor(
        api.search_tweets, q='to:' + curr_replied_user, 
        lang='en', since_id=replied_tweet_.id, 
        tweet_mode="extended", result_type='recent'
    ).items(NUM_PER_REPLY)
    for nested_replied_tweet in replied_replied_tweets:
        if hasattr(nested_replied_tweet, 'in_reply_to_status_id_str'):
            if (nested_replied_tweet.in_reply_to_status_id_str == replied_tweet_.id_str):
                tweet_text = process_text(nested_replied_tweet.full_text)
                if len(all_tweets_replies_) >= NUM_PER_USER:
                    return
                all_tweets_replies_.append(tweet_text)
                try:
                    get_tweet_replies(
                        api, nested_replied_tweet, all_tweets_replies_
                    )
                except Exception as e:
                    print(e)

def get_tweets_user(api, screen_name):
    """For the current user, the first layer is the original tweets, then the direct replies."""
    all_tweets_replies = []
    original_tweets = api.user_timeline(
        screen_name=screen_name, exclude_replies=True
    )
    for original_tweet in original_tweets:
        replied_tweets = tweepy.Cursor(
            api.search_tweets, q='to:' + screen_name, 
            lang='en', since_id=original_tweet.id, 
            tweet_mode="extended", result_type='recent'
        ).items(NUM_PER_TWEET)
        for replied_tweet in replied_tweets:
            if hasattr(replied_tweet, 'in_reply_to_status_id_str'):
                if (replied_tweet.in_reply_to_status_id_str == original_tweet.id_str):
                    tweet_text = process_text(replied_tweet.full_text)
                    if len(all_tweets_replies) >= NUM_PER_USER:
                        return all_tweets_replies
                    all_tweets_replies.append(tweet_text)
                    try:
                        get_tweet_replies(
                            api, replied_tweet, all_tweets_replies
                        )
                    except Exception as e:
                        print(e)
    return all_tweets_replies

def get_tweets_all_users(api):
    """Loop over all users and get map of user and corresponding relies to recent tweets."""
    all_tweets_users = {}
    for screen_name in USERS:
        all_tweets_users[screen_name] = get_tweets_user(api, screen_name)
        print(screen_name + ": ")
        print(all_tweets_users[screen_name])
        print('\n')
    return all_tweets_users


if __name__ == "__main__":
    api = get_api()
    s = OnlineToxicScorer()
    all_tweets_replies = get_tweets_all_users(api)
    for username, tweets_replies in all_tweets_replies.items():
        user_inference = s.inference(tweets_replies)
        print(username + ": ")
        print(user_inference)
        print('\n')
    # inf_array = s.inference(["This is project is a piece of shit", 'Is the inference model on?', "This is a fucking test case!"])
    # print(inf_array)
