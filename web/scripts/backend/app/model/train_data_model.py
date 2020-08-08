from backend.database import db, ma
from typing import List
import datetime
from pytz import timezone

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


class TrainDataModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainDataModel
'''
class TrainDataJoinedModelSchema(ma.SQLAlchemyAutoSchema):
    scrape_id = ma.fields.Integer()
    category_id = ma.fields.Integer()
'''
