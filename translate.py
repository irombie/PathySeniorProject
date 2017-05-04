# -*- coding: utf-8 -*-
import sys
import getopt
from google.cloud import translate
from unidecode import unidecode  # pip install unidecode
from PathyDB import PathyDB

def translate_text(text, model=translate.NMT):
    translate_client = translate.Client()
    result = translate_client.translate(
        text, source_language='tr',
        target_language='eng')
    return result


#print translate_text('hayat sana limon verirse limonata yap')
# api_key='AIzaSyBic5xtcVtZ9rFnAyRMfPISQz_GebwDvBg'


def main(argv):
    table_name = ''
    try:
        opts, args = getopt.getopt(argv, "ut:", ["table="])
    except getopt.GetoptError:
        print 'translate.py -t <table_name>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            print 'translate.py -t <table_name>'
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg

    db = PathyDB()
    tweets = db.get_all_not_translated_tweets(table_name)

    print('Translation begins...')
    for tweet in tweets:
        translated_text = translate_text(unidecode(tweet['normalized_text']))
        print translated_text
        tweet['translated_text'] = translated_text['translatedText']
        db.update_tweet(table_name, tweet)


if __name__ == "__main__":
    main(sys.argv[1:])
