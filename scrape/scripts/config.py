

class SystemConfig:

  MYSQL_DATABASE = "scrape_database"
  MYSQL_PORT= 3306
  MYSQL_USER = "root"
  MYSQL_PASSWORD = "eq967yD5"
  MYSQL_HOST = "db"
  MYSQL_CHARSET = "utf8mb4"
  
  DB_TWITTER_TABLE_NAME = "scrape_data"

  #requestsで使うヘッダー。UAを変えないとあかんサイトがあるので。
  REQUESTS_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

  
  TWITTER_API_CONSUMER_KEY = 'CqfdAxBp3EdHhmcxQ4OTd1Ai9'
  TWITTER_API_CONSUMER_SECRET = 'A3dVp4OtHpCbffkla0sdCisVlgikGOeEnZuOOfamax4Y6Y80vS'
  TWITTER_API_ACCESS_KEY = '850059818656079872-2LewEpk0S35Refz2NaELeIaQ4Ds5URD'
  TWITTER_API_ACCESS_SECRET = 'jEcJT4y7UFYoOQ9M5GqMSciXHunLKtjuEhkhzDbJqHKPk'
  
  
  
  #短縮URL。このリストに含まれているものはすべて展開が必要だとみなして展開を試みる。
  #on.wsj.comとtrib.alはwall street journalで必要。他のサイトでも必要なのが判明ししだい追加してね。
  EXPANDABLE_URLS = ["t.co", "buff.ly", "on.wsj.com","trib.al", "bit.ly", "s.nikkei.com", "sptnkne.ws"]
  
  #このリストに含まれてるURLは中途半端に展開してたりrequestsで扱えないページのURL.
  PROHIBITED_URLS = ["cgi.tbs.co.jp"]

  TWITTER_SCREEN_NAMES = ["nikkei"]


Config = SystemConfig