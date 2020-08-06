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

        # 認証
        auth = tweepy.OAuthHandler(
            Config.TWITTER_API_CONSUMER_KEY,
            Config.TWITTER_API_CONSUMER_SECRET)
        auth.set_access_token(
            Config.TWITTER_API_ACCESS_KEY,
            Config.TWITTER_API_ACCESS_SECRET)

        # tweepy初期化
        #APIの利用制限時（１５分に１８０回のリクエスト超過）に、 必要時間だけ待機する（wait_on_rate_limit = True）
        #利用制限が解除されるのを待っているときに通知を表示する（wait_on_rate_limit_notify = True）
        #通信エラー時のリトライ回数(retry_count)
        self.api = tweepy.API(auth
                              ,wait_on_rate_limit=wait_on_rate_limit
                              ,wait_on_rate_limit_notify=wait_on_rate_limit_notify
                              ,retry_count=retry_count)

        
        
        
        
    def get_tweets_from_screen_names(self, screen_name_list, hours):
        until = datetime.datetime.now().astimezone(timezone('UTC'))
        since = until - datetime.timedelta(hours=hours)

        until_str = until.strftime('%Y-%m-%d_%H:%M:%S_UTC')
        since_str = since.strftime('%Y-%m-%d_%H:%M:%S_UTC')

        textArr = []
        dateArr = []
        nameArr = []
        urlArr = []
        idArr=[]

        for screen_name in screen_name_list:
            try:
                tw = tweepy.Cursor(self.api.search, \
                    q='from:@' + screen_name + ' exclude:retweets', \
                    lang="ja", \
                    count=100, \
                    since=since_str, \
                    until=until_str, \
                    tweet_mode='extended').items() 
                print(tw)
                for j in tw:
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


            except Exception as e:
                print(e)

        ret = pd.DataFrame({'tw_id':idArr,'username':nameArr, 'created_at':dateArr, 'text':textArr, 'url':urlArr})
        return ret