import boto3
from boto3.dynamodb.conditions import Key
from pytest import Item


client = boto3.client('dynamodb')
db = boto3.resource('dynamodb')

__TableUsers__ = "Users"
Primary_Column_Users = "SCREEN_NAME"
table_users = db.Table(__TableUsers__)

__TableTweets__ = "Tweets"
Primary_Column_Tweets = "TWEET_ID"
table_tweets = db.Table(__TableTweets__)

def query_user(screen_name):
    response = table_users.query(
        KeyConditionExpression=Key(Primary_Column_Users).eq(screen_name)
    )
    item = response["Items"]
    return False if len(item) == 0 else True

def query_tweet(tweet_id):
    response = table_tweets.query(
        KeyConditionExpression=Key(Primary_Column_Tweets).eq(tweet_id)
    )
    item = response["Items"]
    return False if len(item) == 0 else True

def insert_tweet(tweet_id, tweet_text, tweet_author):
    table_tweets.put_item(
        Item = {
            Primary_Column_Tweets: tweet_id,
            "TWEET_TEXT": tweet_text,
            "TWEET_AUTHOR": tweet_author
        }
    )


if __name__ == "__main__":
    print(query_tweet(2345678))
    #insert_tweet(2345678, "I want to have dinner!!", "william_tianhao")
