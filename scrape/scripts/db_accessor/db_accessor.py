# -*- coding: utf-8 -*-
import MySQLdb
import os
from config import Config

# DB関連処理共通クラス
class clsDbAccessor():
	# コンストラクタ
	def __init__(self):
		try:
			# 初期化
			self.hasError = False			

			self.connect()
			self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

		except Exception as e:
			print("コンストラクタ　Error!")
			print(e)
			self.hasError = True
			raise ValueError("コンストラクタ Error!")

	def __del__(self):
		self.close()
		
	# コネクトオープン		
	def connect(self):
		conn = MySQLdb.connect(host=Config.MYSQL_HOST,
													port=Config.MYSQL_PORT,
													user=Config.MYSQL_USER,
													passwd=Config.MYSQL_PASSWORD,
													db=Config.MYSQL_DATABASE,
													charset=Config.MYSQL_CHARSET)
													
		self.conn = conn
		return conn


	# コミット
	def commit(self):
		try:
			self.conn.commit()
		except Exception as e:
			print("commit Error!")
			print(e)
			self.hasError = True
			raise ValueError("commit Error!")

	# ロールバック
	def rollback(self):
		try:
			self.conn.rollback()
		except Exception as e:
			print("rollback Error!")
			print(e)
			self.hasError = True
			raise ValueError("rollback Error!")

	# クローズ処理
	def close(self):
		try:
			if self.cursor is not None:
				self.cursor.close()
			if self.conn is not None:
				self.conn.close()
		except Exception as e:
			print("close Error!")
			print(e)
			self.hasError = True
			raise ValueError("close Error!")


	#現在DBにある最新の凸版ニュースサイトからスクレイプした記事のURLとtw_idを取得
	def get_latest_toppan_news_url(self) -> (int,str):
		sql = "select tw_id, url from %s where tw_id=(select max(tw_id) from %s)" % (Config.DB_TWITTER_TABLE_NAME, Config.DB_TWITTER_TABLE_NAME)
		self.cursor.execute(sql)
		result = self.cursor.fetchone()
		
		if result is None:
			return 0, ""
			
		url = result["url"]
		
		return result["tw_id"], url
		
	
	#tbl_twittersにinsert
	def insert_into_twitter_table(self, tw_id, tw_date, text, text_long, url, user_name, og_site_name, og_title, og_description, og_image, created_at):
		sql = "INSERT INTO " + Config.DB_TWITTER_TABLE_NAME + "(tw_id,tw_date,text,text_long,url,user_name, og_site_name, og_title, og_description, og_image, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		self.cursor.execute(sql, (tw_id, tw_date, text, text_long, url, user_name, og_site_name, og_title, og_description, og_image, created_at))
		self.commit()
