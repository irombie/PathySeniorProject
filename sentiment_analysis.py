# -*- coding: utf-8 -*-
import argparse
import sys
import getopt
from google.cloud import language
from unidecode import unidecode  # pip install unidecode
from PathyDB import PathyDB


def print_result(annotations):
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0

    print('Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0


'''
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


analyze('DOSYA_ADI.txt')
'''

def analyze(textToAnalyze):
    """Run a sentiment analysis request on text within a passed filename."""
    language_client = language.Client()
    document = language_client.document_from_html(textToAnalyze)   #TODO bu satır file almadan calısıyor mu bak

    annotations = document.annotate_text(include_sentiment=True,
                                             include_syntax=False,
                                             include_entities=False)

        # Print the results
    print_result(annotations)
    return annotations



def main(argv):
    table_name = ''
    try:
        opts, args = getopt.getopt(argv, "ut:", ["table="])
    except getopt.GetoptError:
        print 'sentiment_analysis.py -t <table_name>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            print 'sentiment_analysis.py -t <table_name>'
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg

    db = PathyDB()
    tweets = db.get_all_not_analyzed_tweets(table_name)
    for tweet in tweets:
        analyzed_text = analyze(unidecode(tweet['translated_text']))  #translate olandan alıyor
        print analyzed_text
        senti_score = analyzed_text.sentiment.score
        tweet['sentiment_score'] = senti_score
        db.update_tweet(table_name, tweet)
    pos,neg=db.get_pos_neg_five(table_name)
    print pos
    print neg
    neg,pos, neut=db.get_perc(table_name)
    print neg
    print pos
    print neut
    time_sent=db.get_time_sent(table_name)
    print time_sent


if __name__ == "__main__":
    main(sys.argv[1:])

