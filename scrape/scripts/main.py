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
  print("scrape start at (UTC)",datetime.datetime.now())
  main()

  print("scrape finish at (UTC)",datetime.datetime.now())
