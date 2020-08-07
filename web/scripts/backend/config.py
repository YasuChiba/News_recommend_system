
class SystemConfig:

  DEBUG = True

  #検索用DB情報
  SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}/{db_name}?charset=utf8mb4'.format(**{
      'user': 'root',
      'password': 'eq967yD5',
      'host': 'db',
      'db_name': 'scrape_database'
  })
  
  JSON_AS_ASCII = False
 

Config = SystemConfig
