from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

class ScrapeDataModel(db.Model):
    __tablename__ = 'scrape_data'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tw_id = db.Column(db.BigInteger, nullable=False)
    user_name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DATETIME, nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    og_site_name = db.Column(db.TEXT, nullable=True)
    og_title = db.Column(db.TEXT, nullable=True)
    og_description = db.Column(db.TEXT, nullable=True)


    def getLatestText() -> str:
      sql = "select * from %s where id=(select max(id) from %s)" % (ScrapeDataModel.__tablename__, ScrapeDataModel.__tablename__)
      val = db.session.execute(sql).first()
      
      if val == None:
        return 0
      else:
        return val["text"]
    
    
    def getAllRecord():
      sql = "select * from %s" % (ScrapeDataModel.__tablename__)
      val = db.session.execute(sql)
      
      schema = ScrapeDataModelSchema(many=True)
      return schema.dump(val)
    
    #hours前までのレコード
    def getRecord(hours):
      until = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
      since = until - datetime.timedelta(hours=hours)
      until_str = until.strftime('%Y-%m-%d %H:%M:%S')
      since_str = since.strftime('%Y-%m-%d %H:%M:%S')

      sql = "select * from %s where created_at between '%s' and '%s'" % (ScrapeDataModel.__tablename__, since_str, until_str)
      val = db.session.execute(sql)
      
      schema = ScrapeDataModelSchema(many=True)
      return schema.dump(val)
    
    #dictのリストを返す
    def getJoinedRecord(hours):
      until = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
      since = until - datetime.timedelta(hours=hours)
      until_str = until.strftime('%Y-%m-%d %H:%M:%S')
      since_str = since.strftime('%Y-%m-%d %H:%M:%S')

      sql = "SELECT scrape_data.*, GROUP_CONCAT(train_data.category_id) FROM scrape_data " + "LEFT JOIN train_data ON scrape_data.id = train_data.scrape_id where created_at between '%s' and '%s' GROUP by scrape_data.id;" % (since_str, until_str)

      val = db.session.execute(sql)

      result = []
      for row in val:
        d = dict(row)
        d["categories"] = d.pop("GROUP_CONCAT(train_data.category_id)", None)
        result.append(d)
      
      return result


class ScrapeDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScrapeDataModel

'''
class ScrapeDataJoinedModelSchema(ma.SQLAlchemyAutoSchema):
  id = ma.fields.Integer()
  tw_id = ma.fields.Integer()
  user_name = ma.fields.String()
  created_at = ma.fields.Date()
  text = ma.fields.String()
  url = ma.fields.String()
  og_site_name = ma.fields.String()
  og_title = ma.fields.String()
  og_description = ma.fields.String()

  pass
'''