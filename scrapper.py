import json
import tweepy
import configparser
import argparse
from decimal import Decimal
from scorer import *
from dynamodb import *


MODEL = OnlineToxicScorer()
NUM_PER_USER = 500
NUM_PER_TWEET = 300
NUM_PER_REPLY = 100
USERS = ["KingJames"]
# USERS = ["william_tianhao", "mikepompeo", "KDTrey5", "SpeakerPelosi", "billieeilish", "willsmith", 
#          "KimKardashian", "BarackObama", "JoeBiden", "TeamPelosi", "AnneeJHathaway", 
#          "CNN", "FoxNews", "nytimes"]

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

def infer_text(tweet_text_):
    model_inference = MODEL.inference([tweet_text_])
    model_inference_list = model_inference.tolist()
    model_scores = [
        json.loads(json.dumps(inference), parse_float=Decimal) for inference in model_inference_list
    ]
    return model_inference, model_scores

def get_tweet_replies_insert(api, replied_tweet_, all_tweets_replies_, screen_name):
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
                model_inference, model_scores = infer_text(tweet_text)
                insert_reply(
                    nested_replied_tweet.id, tweet_text, replied_tweet_.id, model_scores, screen_name
                )
                all_tweets_replies_.append((tweet_text, model_inference))
                try:
                    get_tweet_replies_insert(
                        api, nested_replied_tweet, all_tweets_replies_, screen_name
                    )
                except Exception as e:
                    print(e)

def get_tweets_user_insert(api, screen_name):
    """For the current user, the first layer is the original tweets, then the direct replies."""
    all_tweets_replies = []
    original_tweets = api.user_timeline(
        screen_name=screen_name, exclude_replies=True
    )
    for original_tweet in original_tweets:
        if args.tweet_restriction:
            if (query_tweet(original_tweet.id, False)):
                continue
        insert_tweet(
            original_tweet.id, original_tweet.text, screen_name
        )
        replied_tweets = tweepy.Cursor(
            api.search_tweets, q='to:' + screen_name, 
            lang='en', since_id=original_tweet.id, 
            tweet_mode="extended", result_type='recent'
        ).items(NUM_PER_TWEET)
        for replied_tweet in replied_tweets:
            if args.reply_restriction:
                if (query_reply(replied_tweet.id, False)):
                    continue
            if hasattr(replied_tweet, 'in_reply_to_status_id_str'):
                if (replied_tweet.in_reply_to_status_id_str == original_tweet.id_str):
                    tweet_text = process_text(replied_tweet.full_text)
                    if len(all_tweets_replies) >= NUM_PER_USER:
                        return all_tweets_replies
                    model_inference, model_scores = infer_text(tweet_text)
                    insert_reply(
                        replied_tweet.id, tweet_text, original_tweet.id, model_scores, screen_name
                    )
                    all_tweets_replies.append((tweet_text, model_inference))
                    try:
                        get_tweet_replies_insert(
                            api, replied_tweet, all_tweets_replies, screen_name
                        )
                    except Exception as e:
                        print(e)
    return all_tweets_replies

def get_tweets_all_users(api):
    """Loop over all users and get map of user and corresponding relies to recent tweets."""
    all_tweets_users = {}
    for screen_name in USERS:
        if args.user_restriction:
            if (query_user(screen_name, False)):
                continue
        all_tweets_users[screen_name] = get_tweets_user_insert(api, screen_name)
        print(f"{screen_name}: {len(all_tweets_users[screen_name])}")
        for elem in all_tweets_users[screen_name]:
            print(elem[0])
            print(elem[1])
            print('\n')
        # with open("results_split.txt", 'w') as f:
        #     f.write(f"{screen_name}: {len(all_tweets_users[screen_name])} \n")
        #     for elem in all_tweets_users[screen_name]:
        #         f.write(elem[0] + '\n')
        #         f.write(str(elem[1])[1: -1] + '\n')
        #         f.write('\n')
        #     f.write('\n\n')
    return all_tweets_users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toxic Comment Detector")
    parser.add_argument("--user_restriction", type=bool, default=False)
    parser.add_argument("--tweet_restriction", type=bool, default=False)
    parser.add_argument("--reply_restriction", type=bool, default=False)
    args = parser.parse_args()

    api = get_api()
    all_tweets_replies = get_tweets_all_users(api)
    for username, tweets_replies in all_tweets_replies.items():
        if len(tweets_replies) > 0:
            text = [elem[0] for elem in tweets_replies]
            scores = [elem[1] for elem in tweets_replies]
            print(f"{username}: {len(tweets_replies)}")
            print(scores)
            print('\n')
            # with open("results_merge.txt", 'w') as f:
            #     f.write(f"{username}: {len(tweets_replies)} \n")
            #     f.write(str(text))
            #     for score in scores:
            #         f.write(str(score)[1: -1] + '\n')
            #     f.write('\n')
