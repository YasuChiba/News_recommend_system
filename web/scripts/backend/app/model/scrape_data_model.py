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

class ScrapeDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScrapeDataModel
