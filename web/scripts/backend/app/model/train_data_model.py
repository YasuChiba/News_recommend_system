from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

class TrainDataModel(db.Model):
    __tablename__ = 'scrape_data'
    __table_args__ = {'extend_existing': True}

    scrape_id = db.Column(db.Integer)
    category_id =  db.Column(db.Integer)



class TrainDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScrapeDataModel
'''
class TrainDataJoinedModelSchema(ma.SQLAlchemyAutoSchema):
    scrape_id = ma.fields.Integer()
    category_id = ma.fields.Integer()
'''
