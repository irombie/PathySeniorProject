# -*- coding: utf-8 -*-
import pipeline_caller
import unittest
import os
import re
import sys
import getopt
from unidecode import unidecode  # pip install unidecode
from PathyDB import PathyDB


def main(argv):
    table_name = ''
    token = 'LQiWv0FTmQEJRVbun8Rqld6WZCIrGUyO'
    tool = 'normalize'

    try:
        opts, args = getopt.getopt(argv, "ut:", ["table="])
    except getopt.GetoptError:
        print('normalization.py -t <table_name>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            print('normalization.py -t <table_name>')
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg

    db = PathyDB()
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
    tweets = db.get_all_not_normalized_tweets(table_name)

    for tweet in tweets:
        caller = pipeline_caller.PipelineCaller(tool, unidecode(tweet['tweet_text']), token)
        normalized_text = caller.call()
        print(normalized_text)
        tweet['normalized_text'] = normalized_text
        db.update_tweet(table_name, tweet)


if __name__ == "__main__":
    main(sys.argv[1:])
