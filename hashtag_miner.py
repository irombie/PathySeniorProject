# -*- coding: utf-8 -*-
import urllib
import json
import oauth2
import sys
import getopt
from datetime import datetime
from PathyDB import PathyDB


# Twitter API Access Information
CONSUMER_KEY = 't7esrWcJIyHoV7QtQChdXGsKF'
CONSUMER_SECRET = 'jdTVyyBZpuQVgX1Q7ZBcciWn2Vmqv6IL72fjhOpNVkF6PYzq7J'
key = '725982882704056320-AEjRTxLfl9U9X7KR06Ob5T5baEXWyee'
secret = 'lFnFtbj842vKxfAgRl8HxTcXu1N7YSCAPeg90csV0ENuX'

# Twitter Search API
SEARCH_API_URL = 'https://api.twitter.com/1.1/search/tweets.json?'


# Functions
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content.decode('raw_unicode_escape')


def main(argv):
    # Gets tweets from the specifed hashtag in json format
    # Detailed informaiton: https://dev.twitter.com/rest/reference/get/search/tweets
    hashtag = ''
    lang = ''

    try:
        opts, args = getopt.getopt(argv, "uh:l:", ["hashtag=", "language="])
    except getopt.GetoptError:
        print('hashtag_miner.py -h <hashtag> -l <language>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            print('hashtag_miner.py -h <hashtag> -l <language>')
            sys.exit()
        elif opt in ("-h", "--hashtag"):
            hashtag = '#' + arg
        elif opt in ("-l", "--language"):
            lang = arg

    db = PathyDB()
    table_name = 'tweets_from_' + hashtag[1:]
    table_name=table_name.lower()
    table_name=table_name.replace('ç','c')
    table_name=table_name.replace('Ç','c')
    table_name=table_name.replace('ü','u')
    table_name=table_name.replace('Ü','u')
    table_name=table_name.replace('Ö','o')
    table_name=table_name.replace('Ğ','g')
    table_name=table_name.replace('ü','u')
    table_name=table_name.replace('ğ','g')
    table_name=table_name.replace('Ş','s')
    table_name=table_name.replace('ş','s')
    table_name=table_name.replace('ı','i')
    table_name=table_name.replace('İ','i')

    query = 'q=' + urllib.quote_plus(hashtag) + '&lang=' + lang
    search_url = SEARCH_API_URL + query
    # print search_url

    tweets_json = oauth_req(search_url, key, secret)
    json_data = json.loads(tweets_json)
 
    for cur_tweet in json_data['statuses']:
        temp=cur_tweet['created_at'][4:]
        cre_time=temp.partition('+')[0][:-1]   
        datetime_object = datetime.strptime(cre_time, '%b %d %H:%M:%S')
        if(cur_tweet['place'] is None):
            tweet = {'_id': cur_tweet['id'], 'tweet_text': cur_tweet['text'], 'country': 'none', 'fav':cur_tweet['favorite_count'],'rt':cur_tweet['retweet_count'],'time':datetime_object}
        else:
            tweet = {'_id': cur_tweet['id'], 'tweet_text': cur_tweet['text'], 'country': cur_tweet['place']['country'], 'fav':cur_tweet['favorite_count'],'rt':cur_tweet['retweet_count'],'time':datetime_object}
            
        print(tweet)
        db.insert_into_tweets_table(table_name, tweet)
    
    c_dic =db.count_country(table_name)
    print(c_dic)
    f=db.get_max_fav(table_name)
    print(f)
    r=db.get_max_rt(table_name)
    print(r)
    



if __name__ == "__main__":
    main(sys.argv[1:])
