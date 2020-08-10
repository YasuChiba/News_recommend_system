from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

class CategoryDataModel(db.Model):
    __tablename__ = 'category_data'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    category_name = db.Column(db.TEXT, nullable=False)

    def getAllRecord():
      sql = "select * from %s" % (CategoryDataModel.__tablename__)
      val = db.session.execute(sql)
      
      result = {}
      for row in val:
        d = dict(row)
        result[str(d["id"])] = d["category_name"]
      
      return result

    def insert(category_name):
        sql = "insert into category_data (category_name) values ('%s')" % (category_name)
        db.session.execute(sql)
        db.session.commit()
    
    def delete(category_id):
      sql = "delete from predicted_data where category_id = %s" % (category_id)
      db.session.execute(sql)

      sql = "delete from train_data where category_id = %s" % (category_id)
      db.session.execute(sql)

      sql = "delete from category_data where id = %s" % (category_id)
      db.session.execute(sql)

      db.session.commit()