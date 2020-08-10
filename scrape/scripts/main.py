# -*- coding: utf-8 -*-

from twitter.TwitterScrape import TwitterScrape
import datetime
import requests, json
from config import Config

def main():
  
  twitter_scrape = TwitterScrape()
  try:
    twitter_scrape.start_scrape()
    
  except Exception as e:
    print(e)
  
  
  return
  

if __name__ == '__main__':
  print("===============================================================")
  print("===============================================================")
  text = "scrape start at (UTC)" + str(datetime.datetime.now())
  with open('/root/scrape/logfile.log', 'a') as f:
    print(text, file=f)
  print(text)
  main()

  text = "scrape finish at (UTC)" + str(datetime.datetime.now())
  with open('/root/scrape/logfile.log', 'a') as f:
    print(text, file=f)
  print(text)