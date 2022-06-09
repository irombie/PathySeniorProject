# -*- coding: utf-8 -*-
import urllib
import json
import oauth2
import sys
import getopt
import pipeline_caller
from unidecode import unidecode
from google.cloud import translate
from google.cloud import language
# Twitter API Access Information
CONSUMER_KEY = 't7esrWcJIyHoV7QtQChdXGsKF'
CONSUMER_SECRET = 'jdTVyyBZpuQVgX1Q7ZBcciWn2Vmqv6IL72fjhOpNVkF6PYzq7J'
key = '725982882704056320-AEjRTxLfl9U9X7KR06Ob5T5baEXWyee'
secret = 'lFnFtbj842vKxfAgRl8HxTcXu1N7YSCAPeg90csV0ENuX'
token = 'LQiWv0FTmQEJRVbun8Rqld6WZCIrGUyO'
tool = 'normalize'

# Twitter Search API
SEARCH_API_URL = 'https://api.twitter.com/1.1/search/tweets.json?'


# Functions
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content.decode('raw_unicode_escape')

def translate_text(text, model=translate.NMT):
    translate_client = translate.Client()
    result = translate_client.translate(
    text, source_language='tr',
    target_language='eng')
    return result

def analyze(filename):
    """Run a sentiment analysis request on text within a passed filename."""
    language_client = language.Client()

    with open(filename, 'r') as file:
        document = language_client.document_from_html(file.read())

        annotations = document.annotate_text(include_sentiment=True,
           include_syntax=False,
           include_entities=False)

	# Print the results
    print_result(annotations)
    return annotations

def print_result(annotations):
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))




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
            sys.exit() d
        elif opt in ("-h", "--hashtag"):
            hashtag = '#' + arg
        elif opt in ("-l", "--language"):
            lang = arg

    query = 'q=' + urllib.quote_plus(hashtag) + '&lang=' + lang
    search_url = SEARCH_API_URL + query
    tweets_json = oauth_req(search_url, key, secret)
    json_data = json.loads(tweets_json)
    tweets = []
    for cur_tweet in json_data['statuses']:
        tweets.append({'tweet_id': cur_tweet['id'], 'tweet_text': cur_tweet['text']})

    for i in range(len(tweets)):
        row = tweets[i]
        caller = pipeline_caller.PipelineCaller(tool, unidecode(row['tweet_text']), token)
        normalized_text = caller.call()
        print(row['tweet_text'])
        row['tweet_text']=normalized_text
        print(normalized_text)

    for row in tweets:
        str=translate_text(row['tweet_text'])
        trans_text=str['translatedText']
        row['tweet_text']=trans_text


    f=open('trans_res.txt','w')
    for row in tweets:
        f.write(row['tweet_text']+'\n')
        f.close()
        analyze('trans_res.txt')

if __name__ == "__main__":
    main(sys.argv[1:])

