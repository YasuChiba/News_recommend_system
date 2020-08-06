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
    
  # 挿入したレコード数とエラーメッセージをリターン
  def insertFromDataFrame(self, df: pd.DataFrame) -> str:
    error_message = ""
    
    seq_num = self.getLatestSequenceNumber() + 1
    
    counter = 0
    for index, row in df.iterrows():
      sequence_number=seq_num
      tw_id=int(row["tw_id"])
      user_name=row["username"]
      created_at=row["created_at"]
      text=row["text"]
      text_long=row["text_long"]
      url=row["url"]
      og_site_name=row["og_site_name"]
      og_title=row["og_title"]
      og_description=row["og_description"],
      og_image=row["og_image"]
      
      try:
        sql = "INSERT INTO " + Config.DB_TWITTER_TABLE_NAME + \
              "(sequence_number, tw_id, user_name, created_at, text, text_long, url, og_site_name, og_title, og_description, og_image)" + \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
              
        self.dba.cursor.execute(sql, (sequence_number, tw_id, user_name, created_at, text, text_long, url, og_site_name, og_title, og_description, og_image))
        self.dba.commit()
        counter += 1
        
      except Exception as e:
        error_message += "\n Error at insertFromDataFrame \n" + str(e) + \
                          "user_name: " + user_name + "\n" + "url: "  + url
      
    return counter,error_message
    
    
  def getLatestSequenceNumber(self) -> int:
    
    sql = "select max(sequence_number) from %s" % (Config.DB_TWITTER_TABLE_NAME)
    self.dba.cursor.execute(sql)
    result = self.dba.cursor.fetchone()
    seq_num = result.get("max(sequence_number)")
    if seq_num is None:
      return 0
    else:
      return seq_num
    
    
  
  def isExistTweetID(self, tw_id: int) -> bool:
    
    sql = "select * from twitter_data where tw_id = " + str(tw_id) + " limit 1"
    self.dba.cursor.execute(sql)
    val = self.dba.cursor.fetchone()

    if val == None or len(val) == 0:
      return False
    
    return True
    