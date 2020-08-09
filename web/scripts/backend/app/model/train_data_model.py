from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

from .scrape_data_model import ScrapeDataModel

class TrainDataModel(db.Model):
    __tablename__ = 'train_data'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scrape_id = db.Column(db.Integer)
    category_id =  db.Column(db.Integer)

    def delete(scrape_id, category_id):
        scrape_id = int(scrape_id)
        category_id = int(category_id)
        sql = "delete from train_data where scrape_id = %s and category_id = %s" % (scrape_id, category_id)
        db.session.execute(sql)
        db.session.commit()

    def insert(scrape_id, category_id):
        scrape_id = int(scrape_id)
        category_id = int(category_id)
        sql = "insert into train_data (scrape_id, category_id) values (%s, %s)" % (scrape_id, category_id)
        print(sql)
        db.session.execute(sql)
        db.session.commit()



    def getRecordFromCategoryIDWithJoin(category_id, hours):

        until = ScrapeDataModel.getLatestPostedDate()
        since = until - datetime.timedelta(hours=hours)
        until_str = until.strftime('%Y-%m-%d %H:%M:%S')
        since_str = since.strftime('%Y-%m-%d %H:%M:%S')


        sql = "select scrape_data.*, train_data.category_id from train_data join scrape_data on train_data.scrape_id = scrape_data.id " \
        "where scrape_data.created_at between '%s' and '%s' and train_data.category_id = %s" % (since_str, until_str, category_id)

        print(sql)
        val = db.session.execute(sql)

        result = []
        for row in val:
          d = dict(row)
          result.append(d)

        return result


class TrainDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainDataModel
'''
class TrainDataJoinedModelSchema(ma.SQLAlchemyAutoSchema):
    scrape_id = ma.fields.Integer()
    category_id = ma.fields.Integer()
'''
