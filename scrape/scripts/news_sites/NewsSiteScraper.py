# -*- coding: utf-8 -*-


from config import Config
from typing import List
import requests
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import time
from selenium import webdriver


#各ニュースサイトのメインコンテンツをスクレイプ
class NewsSiteScraper():
  
  def __init__(self):
   
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')

    self.selenium_driver = webdriver.Chrome("/root/scrape_script/lib/chromedriver", options=options)
    
  def __del__(self):
    self.selenium_driver.close()
    self.selenium_driver.quit()
  
  
  #urlを受け取ってそれに対応するメインコンテンツを返す。スクレイプ出来なければNoneを返す
  #urlは展開してないものでもしたものでもどっちでも良い。返り値に入ってるurlは展開されたもの。
  # 返り値: url, og_site_name, og_title, og_description
  def scrape(self, url:str) -> (str, str, str, str):
    
    url = self._expand_url(url)
    parsed_url = urlparse(url)
    try:
      if parsed_url.netloc in Config.EXPANDABLE_URLS:
        #この時点で展開されてないURLのとき（つまりrequestsじゃ扱えないとき）
        self.selenium_driver.get(url)
        url = self.selenium_driver.current_url
        parsed_url = urlparse(url)
        html = self.selenium_driver.page_source.encode('utf-8')
        soup = bs4(html, "html.parser")
      else:
        req = requests.get(url, headers=Config.REQUESTS_HEADER)
        soup = bs4(req.content, "html.parser")
        parsed_url = urlparse(req.url)
    except Exception as e:
      raise ValueError("cannot fetch page\n"+ str(e))

    #OGPタグの取得
    og_site_name, og_title, og_description = self._get_ogp_content(soup)

    
    return url, og_site_name, og_title, og_description
  
  
    
  #OGPタグのコンテンツを取得
  def _get_ogp_content(self, soup):
    og_site_name = None
    og_title = None
    og_description = None
              
    #og:site_name
    og_site_name_elem = soup.find('meta', attrs={'property': 'og:site_name'})
    if (og_site_name_elem is not None) and (og_site_name_elem.get("content") is not None):
      og_site_name = og_site_name_elem["content"]
      
    #og:title
    og_title_elem = soup.find('meta', attrs={'property': 'og:title'})
    if (og_title_elem is not None) and (og_title_elem.get("content") is not None):
      og_title = og_title_elem["content"]
      
    #og:description
    og_description_elem = soup.find('meta', attrs={'property': 'og:description'})
    if (og_description_elem is not None) and (og_description_elem.get("content") is not None):
      og_description = og_description_elem["content"]
      
    return og_site_name, og_title, og_description

  

  #短縮URLかどうか判定。
  #展開可能な短縮URLだったら本来アクセスする場所のURLを返す。
  #普通のURLだったらそのまま返す
  #展開不可能なやつもそのまま返す
  #再帰だとわかりにくくなるのでループでやるために関数２つに別れてる
  def _expand_url(self, url: str) -> str:
    
    _url = url
    #最大５回展開を試みる
    for i in range(5):
      parsed_url = urlparse(_url)
      #展開可能な短縮URLかどうかを判定
      if parsed_url.netloc in Config.EXPANDABLE_URLS:

        #展開してみて、Noneが返ってきたらやめて外に出てもとのURLを返す
        #URLだったら更に展開してみる
        _url = self.__expand_url(_url)
        if _url is None:
          _url = url
          break  
      else:
        break
    
    return _url


  #展開可能なものであれば展開してかえす
  #不可ならNoneがかえる
  def __expand_url(self, url: str) -> str:

    parser_url = urlparse(url)
    resp = requests.get(url, allow_redirects=False, timeout=5)

    _url = None 
    if 'Location' in resp.headers and (300 <= resp.status_code < 400):
      _url = resp.headers['Location']
      parsed_url = urlparse(_url)
      #取得したリダイレクト先のURLがほんとにアクセスしたい場所でないときはもとのURL使う.そうでなければ更新
      if parsed_url.netloc in Config.PROHIBITED_URLS:
        _url = None 
      else:
        url = _url

    return _url

  
