from flask import Flask, render_template, request, Blueprint, current_app, jsonify
from .model.scrape_data_model import ScrapeDataModel
from .model.category_data_model import CategoryDataModel

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/test',methods=['GET'])
def test():
  text = ScrapeDataModel.getLatestText()
  
  return text
  

@api_blueprint.route('/test2',methods=['GET'])
def test2():
  text = ScrapeDataModel.getRecord(5)
  
  return jsonify(text), 200


@api_blueprint.route('/test3',methods=['GET'])
def test3():
  scrape_data = ScrapeDataModel.getJoinedRecord(10)

  categories = CategoryDataModel.getAllRecord()
  print(categories.values())

  for data in scrape_data:
    _cat = data["categories"]

    _categories = []
    if _cat is not None:
        _cat = _cat.split(",")
        _categories = []
        for _c in _cat:
            _categories.append(categories[str(_c)])
        
    _categories_dic = {}
    for cat in categories.values():
        _categories_dic[cat] = 1 if cat in _categories else 0

    data["categories"] = _categories_dic

    
    
  
  return jsonify(scrape_data), 200
