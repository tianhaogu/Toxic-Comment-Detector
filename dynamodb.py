from decimal import Decimal
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
import json
from pytest import Item


client = boto3.client('dynamodb')
db = boto3.resource('dynamodb')

__TableUsers__ = "Users"
Primary_Column_Users = "SCREEN_NAME"
table_users = db.Table(__TableUsers__)

__TableTweets__ = "Tweets"
Primary_Column_Tweets = "TWEET_ID"
table_tweets = db.Table(__TableTweets__)

__TableReplies__ = "Replies"
Primary_Column_Replies = "REPLY_ID"
table_replies = db.Table(__TableReplies__)

def query_user(screen_name, whether_extract):
    response = table_users.query(
        KeyConditionExpression=Key(Primary_Column_Users).eq(screen_name)
    )
    item = response["Items"]
    if not whether_extract:
        return False if len(item) == 0 else True
    return item

def query_tweet(tweet_id, whether_extract):
    response = table_tweets.query(
        KeyConditionExpression=Key(Primary_Column_Tweets).eq(tweet_id)
    )
    item = response["Items"]
    if not whether_extract:
        return False if len(item) == 0 else True
    return item

def insert_tweet(tweet_id, tweet_text, tweet_author):
    table_tweets.put_item(
        Item = {
            Primary_Column_Tweets: tweet_id,
            "TWEET_TEXT": tweet_text,
            "TWEET_AUTHOR": tweet_author
        }
    )

def query_reply(reply_id, whether_extract):
    response = table_replies.query(
        KeyConditionExpression=Key(Primary_Column_Replies).eq(reply_id)
    )
    item = response["Items"]
    if not whether_extract:
        return False if len(item) == 0 else True
    return item

def insert_reply(reply_id, reply_text, reply_to_id, scores, screen_name):
    table_replies.put_item(
        Item = {
            Primary_Column_Replies: reply_id,
            "REPLY_TEXT": reply_text,
            "REPLY_TO_ID": reply_to_id,
            "SCORES": scores,
            "ORIGINAL_AUTHOR": screen_name
        }
    )

def update_score(reply_id, scores):
    table_replies.update_item(
        Key = {
            "REPLY_ID": reply_id
        },
        UpdateExpression = "set SCORES=:s",
        ExpressionAttributeValues = {
            ":s": scores
        }
    )


if __name__ == "__main__":
    original_scores = [0.1645, 0.33245, 0.0389, 0.1356, 0.344564, 0.131]
    curr_scores = [json.loads(json.dumps(score), parse_float=Decimal) for score in original_scores]
    update_score(23452453, curr_scores)
    #insert_tweet(2345678, "I want to have dinner!!", "william_tianhao")
