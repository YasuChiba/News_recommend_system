# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tweepy
import datetime
from tweepy.error import TweepError
from pytz import timezone

import time
import calendar
import re
from config import Config


class TweepyController:
    def __init__(self):
   
        wait_on_rate_limit = True
        wait_on_rate_limit_notify = True
        retry_count = 5

        # ログイン設定
        twitter_conf = {
            'consumer' : {
                'key'    : Config.TWITTER_API_CONSUMER_KEY,
                'secret' : Config.TWITTER_API_CONSUMER_SECRET
            },
            'access'   : {
                'key'    : Config.TWITTER_API_ACCESS_KEY,
                'secret' : Config.TWITTER_API_ACCESS_SECRET
            }
        }

        # 認証
        auth = tweepy.OAuthHandler(
            twitter_conf['consumer']['key'],
            twitter_conf['consumer']['secret'])
        auth.set_access_token(
            twitter_conf['access']['key'],
            twitter_conf['access']['secret'])

        # tweepy初期化
        #APIの利用制限時（１５分に１８０回のリクエスト超過）に、 必要時間だけ待機する（wait_on_rate_limit = True）
        #利用制限が解除されるのを待っているときに通知を表示する（wait_on_rate_limit_notify = True）
        #通信エラー時のリトライ回数(retry_count)
        self.api = tweepy.API(auth
                              ,wait_on_rate_limit=wait_on_rate_limit
                              ,wait_on_rate_limit_notify=wait_on_rate_limit_notify
                              ,retry_count=retry_count)

    #hours前のツイートから取得
    def get_my_friends_tweet(self, hours):
        # 自分のID
        my_info = self.api.me()
        return self.get_friends_tweet(my_info.id, hours)

    def get_friends_tweet(self, ID, hours):
        friends_ids = []
        for id in tweepy.Cursor(self.api.friends_ids, id=ID).items():
            friends_ids.append(id)

        self.ID=ID
        return self.get_tweet(friends_ids,hours)

    def get_tweet(self, friends_ids, hours):
        # ツイート取得日付（直近１週間）
      
        
        until = datetime.datetime.now().astimezone(timezone('UTC'))
        since = until - datetime.timedelta(hours=hours)

        until_str = until.strftime('%Y-%m-%d_%H:%M:%S_UTC')
        since_str = since.strftime('%Y-%m-%d_%H:%M:%S_UTC')
        #print(until_str)
        #print(since_str)
        
        textArr = []
        dateArr = []
        nameArr = []
        urlArr = []
        idArr=[]

        user_count = 0
        #print("frineds_ids")
        #friends_ids = [friends_ids[2], friends_ids[3], friends_ids[4], friends_ids[5]]
        #friends_ids = [friends_ids[3]]
        #print(friends_ids)
        # 100IDsずつに詳細取得
        for i in range(0, len(friends_ids), 100):

            for user in self.api.lookup_users(user_ids=friends_ids[i:i+100]):
                start_time = time.time()
                user_count = user_count + 1
                #print(user.name)

                try:
                    #print('{}:user.name={}, user.screen_name={}, user.statuses_count={}, user.id={}'.format(user_count, user.name, user.screen_name, user.statuses_count, user.id))
                    
                    # api.search：公式サイトで取得制限は過去１週間記載。が、10日前まで取れてる。countは１リクエストごとに取得する件数（MAX１００件）
                    tw = tweepy.Cursor(self.api.search, \
                        q='from:@' + user.screen_name + ' exclude:retweets', \
                        lang="ja", \
                        count=100, \
                        since=since_str, \
                        until=until_str, \
                        tweet_mode='extended').items()
                        
                    tweet_count = 0

                    for j in tw:
                        tweet_count=tweet_count+1
                        # ツイート内の改行を削除
                        status = str(j.full_text).replace("\n","")
                        # 正規表現でURLを除外
                        status = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%]+)", "", status)
                        textArr.append(status)
                        idArr.append(j.id)
                        #  UTC（世界標準時）で返ってくるので日本時間にするために9時間プラス
                        j.created_at += datetime.timedelta(hours=9)
                        dateArr.append(j.created_at)
                        nameArr.append(j.user.name)
                        if j.entities['urls']:
                            urlArr.append(j.entities['urls'][0]['url'])
                        else:
                            urlArr.append('')
                       # if 3 <= tweet_count:
                        #    break

                except TweepError as e:
                    print('user.name={}, error:{}'.format(user.name, e.reason))
                    pass

                search_time = time.time() - start_time
                #print ("  search_time:{:8.1f}[sec], tweet_count:{}".format(search_time, tweet_count))

        ret = pd.DataFrame({'tw_id':idArr,'username':nameArr, 'created_at':dateArr, 'text':textArr, 'url':urlArr})
        return ret
        
        
        
        