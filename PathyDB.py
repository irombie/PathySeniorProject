# -*- coding: utf-8 -*-
import sys
import csv
import operator
import pymongo

class PathyDB():
    """docstring for PathyDB."""
    __db_user = 'irem'
    __db_pass = 'felispathy'
    __url = "mongodb://{}:{}@ds149489.mlab.com:49489/pathydb".format(__db_user, __db_pass)

    def __init__(self):
        self.conn = pymongo.mongo_client.MongoClient(host = PathyDB.__url).get_default_database()

    def insert_into_tweets_table(self, table_name, tweet):
        self.conn[table_name].insert(tweet)

    def get_all_not_normalized_tweets(self, table_name):
        return self.conn[table_name].find({'normalized_text': {'$exists': False}})

    def get_all_not_translated_tweets(self, table_name):
        return self.conn[table_name].find({
            'normalized_text': {'$exists': True},
            'translated_text': {'$exists': False},
        })

    def get_all_not_analyzed_tweets(self, table_name):
        return self.conn[table_name].find({
            'normalized_text': {'$exists': True},
            'translated_text': {'$exists': True},
            'sentiment_score': {'$exists': False}
        })

    def update_tweet(self, table_name, tweet):
        self.conn[table_name].find_one_and_update({'_id': tweet['_id']}, {"$set": tweet})
    def count_country(self, table_name):
        cnt=[]
        count_dic={}
        cts=self.conn[table_name].distinct('country');
        for i in range(0,len(cts)):
            cnt.append(0)
        for i in range(0,len(cts)):
            for x in self.conn[table_name].find( { 'country': cts[i] } ):
                cnt[i]=cnt[i]+1;
        for i in range(0,len(cts)):
            count_dic[cts[i]]= cnt[i]
        with open('pie-data.csv', 'wb') as csv_file: 
            writer = csv.writer(csv_file)
            writer.writerow(['Country', 'Occurence'])
            for key, value in count_dic.items():
                writer.writerow([key, value])
        return count_dic
    def get_max_fav(self, table_name):
        max=0
        fav_tw=''
        for t in self.conn[table_name].find():
            if t['fav']>max:
                max=t['fav']
                fav_tw=t['tweet_text']
        return fav_tw
    def get_max_rt(self, table_name):
        max=0
        rt_tw=''
        for t in self.conn[table_name].find():
            if t['rt']>max:
                max=t['rt']
                rt_tw=t['tweet_text']
        return rt_tw
    def get_pos_neg_five(self, table_name):
        temp={}
        for t in self.conn[table_name].find():
            temp[t['tweet_text']]=t['sentiment_score']
        sorted_scores= sorted(temp.items(), key=operator.itemgetter(1))
        pos={}
        neg={}
        for i in range(0,5):
            neg[i]=sorted_scores[i]
        for i in range(len(sorted_scores)-5,len(sorted_scores)):
            pos[i]=sorted_scores[i]
        return pos,neg
    def get_perc(self,table_name):
        neg_c=0
        pos_c=0
        neut_c=0
        for t in self.conn[table_name].find():
            if t['sentiment_score']<=0.3 and t['sentiment_score']>=-0.3:
                neut_c=neut_c+1
            elif t['sentiment_score']<-0.3:
                neg_c=neg_c+1
            else:
                pos_c=pos_c+1
        return neg_c, pos_c,neut_c
    def get_time_sent(self, table_name):
        time_sent={}
        for t in self.conn[table_name].find():
            time_sent[t['time']]=t['sentiment_score']
        time_sent1=sorted(time_sent.items(), key=operator.itemgetter(0))
        return time_sent1

## TEST CODE
def main():
    db = PathyDB()
    #db.insert_into_tweets_table('deneme', tweet)

if __name__ == "__main__":
    main()
