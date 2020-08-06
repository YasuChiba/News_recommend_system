# -*- coding: utf-8 -*-

from db_accessor import clsDbAccessor
from config import Config
import pandas as pd

class TwitterDBAccessor:
  
  
  def __init__(self):
    self.dba = clsDbAccessor()
    
  #やんなくてもいいけど一応。
  def __del__(self):
    del self.dba
    
  def insertFromDataFrame(self, df: pd.DataFrame):
    error_message = ""
        
    for index, row in df.iterrows():
      tw_id=int(row["tw_id"])
      user_name=row["username"]
      created_at=row["created_at"]
      text=row["text"]
      url=row["url"]
      og_site_name=row["og_site_name"]
      og_title=row["og_title"]
      og_description=row["og_description"],
      
      try:
        sql = "INSERT INTO " + Config.DB_TWITTER_TABLE_NAME + \
              "(tw_id, user_name, created_at, text, url, og_site_name, og_title, og_description)" + \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
              
        self.dba.cursor.execute(sql, (tw_id, user_name, created_at, text, url, og_site_name, og_title, og_description))
        self.dba.commit()
        
      except Exception as e:
        print(e)
      
    return 
    
    
  
  def isExistTweetID(self, tw_id: int) -> bool:
    
    sql = "select * from " +Config.DB_TWITTER_TABLE_NAME + " where tw_id = " + str(tw_id) + " limit 1"
    self.dba.cursor.execute(sql)
    val = self.dba.cursor.fetchone()

    if val == None or len(val) == 0:
      return False
    
    return True
    