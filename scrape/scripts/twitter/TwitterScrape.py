# -*- coding: utf-8 -*-


from .TweepyController import TweepyController
from .TwitterDBAccessor import TwitterDBAccessor
from news_sites.NewsSiteScraper import NewsSiteScraper
from config import Config

import os
import pandas as pd
import numpy as np
import datetime
import requests
from urllib.parse import urlparse
import traceback

class TwitterScrape:
  def __init__(self):
    
    self.dba = TwitterDBAccessor()

  def start_scrape(self):

    tw_data = TweepyController().get_tweets_from_screen_names(Config.TWITTER_SCREEN_NAMES,6)
    if len(tw_data) == 0:
      return 
    
    tw_data = self._data_shaping(tw_data)
    
    #列を追加
    tw_data['og_site_name'] = pd.Series().astype(str)
    tw_data['og_title'] = pd.Series().astype(str)
    tw_data['og_description'] = pd.Series().astype(str)
    
    #text_longとOGPを埋める
    tw_data = self._scrape_detail(tw_data)

    #DBへの挿入
    try:
      self.dba.insertFromDataFrame(tw_data)
      return 
      
    except Exception as e:
      print(e)
      return 
          

  #データの整形
  def _data_shaping(self,tw_data: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    
    tw_data.dropna(subset=['url'], inplace=True)  
    #urlの長さが０のやつも除外
    tw_data = tw_data[tw_data["url"].apply(lambda x: len(str(x)) > 0)].copy()
    
    #すでにDBに存在するものは削除
    for index, row in tw_data.iterrows():
      result = self.dba.isExistTweetID(row["tw_id"])
      if result:
        tw_data.drop(index=index, inplace=True)
      
    tw_data = tw_data.sort_values('created_at', ascending=False)
    
    tw_data.reset_index(drop=True, inplace=True)
    return tw_data
  
  
  #スクレイプしてきてtext_longとogpタグを埋める.　エラーメッセージも返す
  def _scrape_detail(self, tw_data: pd.core.frame.DataFrame) -> (pd.core.frame.DataFrame, str):
    error_message = ""
    
    scraper = NewsSiteScraper()

    for index, row in tw_data.iterrows():
      url = row["url"]
      og_site_name = None
      og_title = None
      og_description = None
      
      try:
        url, og_site_name, og_title, og_description = scraper.scrape(url)
      except Exception as e:
        print(e)
        
      tw_data.at[index, "url"] = url
      tw_data.at[index, "og_site_name"] = og_site_name
      tw_data.at[index, "og_title"] = og_title
      tw_data.at[index, "og_description"] = og_description
  
    return tw_data
  
  
