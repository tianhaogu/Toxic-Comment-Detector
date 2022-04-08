import requests
import os
import json
import tweepy
import configparser

#  TODO: Currently waiting for elevated access of Twitter API to be approved, and only write some sketch (eg. only one example user)
#        to test the current functionality. Next need to consider more targeted users and think about how to connect with DynamoDB (eg. for ID Deduplication)
#        Then, need to auto-crawl (eg. use while True?) and consider crawling limits.

# def get_api():
#     config = configparser.ConfigParser()
#     config.read('config.ini')

#     api_key = config['twitter']['api_key']
#     api_key_secret = config['twitter']['api_key_secret']
#     access_token = config['twitter']['access_token']
#     access_token_secret = config['twitter']['access_token_secret']

#     auth = tweepy.OAuthHandler(api_key, api_key_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth, wait_on_rate_limit=True)
#     return api

# def get_replies(screen_name, tweet, curr_tweet_replies):
#     '''Use recursion to get all replies of the original tweet, and all nested replies of each reply'''
#     number_of_replies = 50
#     tweet_replies = tweepy.Cursor(
#         api.search, q='to:' + screen_name, since_id=tweet.id, tweet_mode="extended", lang='en'
#     ).items(number_of_replies)
#     for reply_tweet in tweet_replies:
#         if hasattr(tweet, 'in_reply_to_status_id_str'):
#             if (reply_tweet.in_reply_to_status_id_str == tweet.id_str):
#                 curr_tweet_replies.append(reply_tweet.text)
#                 try:
#                     reply_tweet_user_name = reply_tweet.user.screen_name
#                     for reply_to_reply in get_replies(reply_tweet_user_name, reply_tweet, curr_tweet_replies):
#                         pass
#                 except Exception:
#                     pass
#     return curr_tweet_replies

# def get_tweets(api, screen_name):
#     all_tweets_replies = []
#     number_of_tweets = 200
#     user_tweets = tweepy.Cursor(
#         api.user_timeline, screen_name=screen_name, tweet_mode="extended"
#     ).items(number_of_tweets)
#     for tweet in user_tweets:
#         curr_tweet_replies = []
#         all_tweets_replies.append(get_replies(screen_name, tweet, curr_tweet_replies))
#     return all_tweets_replies


if __name__ == "__main__":
    mylst = ['Strong black woman scare you. Sting black women inspire young girls. Who do you inspire, Mike?? https://t.co/Gb7SHLRIDg', 'Nobody cares about Mike Pompeo’s opinion any more. Somebody really needs to let Mike know.', "Said the party who confirmed justice Kavanaugh! We all know the REAL reason most of the GOP voted against judge Jackson's confirmation.", 'The mayor of D.C. and Nancy Pelosi are in charge,” Trump said of the Jan. 6, 2021, riot to the Washington Post. So now Trump is saying that Pelosi had more power than him at the time? Interesting...', 'You’re a sorry excuse for a human, Mike. You sold out your country and democracy for a grasp at power and you failed.', 'Well said', 'How can anyone today say how it is written? No one knows the intent of the writer. We have fashioned our interpretations how we see fit. Example is the 2nd amendment. Soon rocket propelled grenades will be acceptable. Get off it Mike.', 
    'There may be a overwhelming need 2 rewrite US constitution like that of France 2 avert completely future possibilities of radical libtards playing havoc with future of US democracy, overtaking control through rampant Muslim pandering, Chinese appeasers n destabilise global order', 'Rot of obsession with establishing n protecting Global Liberal order weirdly based nt on absurd global US dominance bt need fr ultimate destruction of Western democracies n in particular US Democracy through utter Muslim pandering even as per Robert Spencer of DailyJihad Watch', "No cares what you think we are just happy you're gone.", 'How come no one of these great Jurist ever speak of John Marshall', 'Fortunately you had no say so in the matter 😶', 'I don’t care how much weight you lost - you will never be President.', 'Say goodbye to your rights ladies. Hang on to your muskets gentlemen. #ConstitutionWins', 'Never trade with dictatorship Don’t let Russia and China dictatorship destroy our world Let’s fight against dictatorship Fight for freedom #StandWithUkraine #DefendUkraine #PutinWarCrimes', 'You forgot to mention how much god inspires you. JS. 🤷🤷\u200d♀️🤷\u200d♂️', 
    "That's what President Biden &amp; the Democratic Congress has been doing since January 20, 2021.", 'Mike I read some of the terrible responses to your twitter. Don’t worry about any of them, they are probably not very high on intelligence chart. Carry on.', 'That is so far from the truth.', 'You are a true Patriot. Our country needs you. I appreciate your service.', 'You will not be President.', 'Thank you for your steadfast belief in America, the country that has made the world better, more than any other, since its founding, through the spread of democracy, freedom, creativity, innovation, and inclusion. Keep up the great work! Hope you run for POTUS.', 'Please don’t give up, we need more leaders like you to survive this Biden term. Now more than ever.', 'I don’t think you can count on the Biden administration for much of anything except more people crossing our borders. Why didn’t Trump fix immigration policy?', 'We are counting on leadership like you or we are doomed.']
    print(len(mylst))
    # api = get_api()
    # screen_name = "william_tianhao"
    # all_tweets_replies = get_tweets(api, screen_name)
    # for curr_tweet_replies in all_tweets_replies:
    #     print(curr_tweet_replies)
    #     print('\n')

    # statuses = api.user_timeline(screen_name=screen_name, exclude_replies=True) 
    # for status in statuses:
    #     print(status.text, end = "\n")
    #     print('\n')
    # for tweet in tweepy.Cursor(api.search_tweets, q='to:' + screen_name, tweet_mode="extended", result_type='recent').items(number_of_tweets):
    #     print(tweet.full_text)
    #     if hasattr(tweet, 'in_reply_to_status_id_str'):
    #         print(tweet.in_reply_to_status_id_str, '    ', tweet.id_str)
    #         print('---------------------------------')
    #         if (tweet.in_reply_to_status_id_str == tweet.id_str):
    #             all_tweets_replies.append(tweet)
    # print(all_tweets_replies)
