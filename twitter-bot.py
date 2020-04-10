import time
import tweepy
import logging

#Here you have to use your auth keys from twitter API, just google Twitter Developer and follow the instructions to get your own key!
auth = tweepy.OAuthHandler('xxxxxx','yyyyyy')
auth.set_access_token('zzzzzzz','wwwwww')


api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

user = api.me()

mentions = api.mentions_timeline()

FILE_NAME = 'last_seen_id.txt'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()
            if not tweet.favorited:
                tweet.favorite()
            try:
                api.update_status('@' + tweet.user.screen_name +
                              ' Obrigada por interagir comigo, fique em casa e não escute o bolsonaro!', in_reply_to_status_id = tweet.id)
            except Exception as e:
                logger.error("Error on reply -duplicated-", exc_info=True)
    return new_since_id


search = 'cloroquina'
nrTweets = 2300
since_id = 1

for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
    if not tweet.favorited:
        try:
            tweet.favorite()
            print('Tweet Liked')
        except Exception as e:
            logger.error("Error on fav", exc_info = True)
    if not tweet.retweeted:
        try:
            tweet.retweet()
            print('Tweet Retweeted')
        except Exception as e:
            logger.error("Error on retweet", exc_info=True)    
    time.sleep(45)
    since_id = check_mentions(api, 'ola', since_id)
    time.sleep(10)
    
