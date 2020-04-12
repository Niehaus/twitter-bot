import requests
import time
import tweepy
import logging

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')

# Request fails unless we provide a user-agent
api_response = requests.get('https://thevirustracker.com/free-api?countryTotal=BR', headers={"User-Agent": "Chrome"})
covid_stats = api_response.json()['countrydata']

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
user = api.me()
mentions = api.mentions_timeline()

FILE_NAME = 'last_seen_id.txt'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

search = ['cloroquina', 'virus chines']
nrTweets = 2300
total_cases = covid_stats[0]["total_cases"]
total_deaths = covid_stats[0]["total_deaths"]
danger_rank = covid_stats[0]["total_danger_rank"]

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    keywords = ['coronga no brasil', 'corona virus no brasil',
                'corona vírus no brasil', 'covid-19 no brasil', 'covid 19 no brasil']
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if 'coronga no brasil' or 'corona virus no brasil' or 'corona vírus no brasil' or 'covid-19 no brasil' or 'covid 19 no brasil' in mention.full_text.lower():
            print('found keyword', flush=True)
            if not mention.favorited:
                try:
                    mention.favorite()
                    print('Mention Liked')
                except Exception as e:
                    logger.error("Error on fav", exc_info=True)
            print('responding back to ' + mention.user.screen_name, flush=True)
            api.update_status('@' + mention.user.screen_name + ' Dados da COVID-19 no Brasil atualmente: \n\n' +
                              "\tTotal de Casos: " + str(total_cases) + "\n" + "\tTotal de Mortes: "+ str(total_deaths) + "\n" + 
                              "\tRanking de Perigo do País atualmente: " + str(danger_rank) + "\n\nDados coletados em https://thevirustracker.com", mention.id)


# Break out individual stats   if any(keyword in tweet.text.lower() for keyword in keywords):
#print("Total de Casos:", covid_stats[0]["total_cases"])
#print("Total de Mortes:", covid_stats[0]["total_deaths"])
#print("Ranking de Perigo do País atualmente:", covid_stats[0]["total_danger_rank"])
print( 'Dados da COVID-19 no Brasil atualmente: \n' +
      "Total de Casos: " + str(total_cases) + "\n" + "Total de Mortes: " + str(total_deaths) + "\n" +
      "Ranking de Perigo do País atualmente: " + str(danger_rank))
while True:
    reply_to_tweets()
    time.sleep(15)

'''
while(True):
    since_id = check_mentions(api, 'Fala comigo', since_id)
    time.sleep(20)
Obrigada por interagir comigo, fique em casa e não escute o bolsonaro!
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
    
    #time.sleep(15)
    
'''
