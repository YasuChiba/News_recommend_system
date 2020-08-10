from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

from .scrape_data_model import ScrapeDataModel

class PredictedDataModel(db.Model):
    __tablename__ = 'predicted_data'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scrape_id = db.Column(db.Integer)
    category_id =  db.Column(db.Integer)
    probability =  db.Column(db.Float)

    #min_scrape_idより小さいscrape_idのレコードをかえす。Noneのときは頭から５件
    def getRecordFromCategoryIDWithJoin(category_id, min_scrape_id):

        sql = "select scrape_data.*, predicted_data.category_id, predicted_data.probability from predicted_data join scrape_data on predicted_data.scrape_id = scrape_data.id " 

        if min_scrape_id is not None:
            sql += "where scrape_data.id < %s and " % (min_scrape_id)
        else:
            sql += "where "

        sql += "predicted_data.category_id = %s order by scrape_data.id DESC LIMIT 5" % (category_id)

        print(sql)
        val = db.session.execute(sql)

        result = []
        for row in val:
          d = dict(row)
          result.append(d)

        return result


class PredictedDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PredictedDataModel
'''
class TrainDataJoinedModelSchema(ma.SQLAlchemyAutoSchema):
    scrape_id = ma.fields.Integer()
    category_id = ma.fields.Integer()
'''
