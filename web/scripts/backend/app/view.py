from flask import Flask, render_template, request, Blueprint, current_app, jsonify, json
from .model.scrape_data_model import ScrapeDataModel
from .model.category_data_model import CategoryDataModel
from .model.train_data_model import TrainDataModel
from .model.predicted_data_model import PredictedDataModel

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/test',methods=['GET'])
def test():
  text = ScrapeDataModel.getLatestText()
  
  return text
  

@api_blueprint.route('/test2',methods=['GET'])
def test2():
  text = ScrapeDataModel.getRecord(5)
  
  return jsonify(text), 200


@api_blueprint.route('/news_data',methods=['GET'])
def news_data():
  min_scrape_id = request.args.get("min_scrape_id")
  scrape_data = ScrapeDataModel.getJoinedRecord(min_scrape_id)

  categories = CategoryDataModel.getAllRecord()

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
        _categories_dic[cat] = True if cat in _categories else False

    data["categories"] = _categories_dic

  return jsonify(scrape_data), 200

@api_blueprint.route('/news_data/annotated_category',methods=['GET'])
def annotated_news_data_category():
    category_id = request.args.get("category_id")
    min_scrape_id = request.args.get("min_scrape_id")

    result = TrainDataModel.getRecordFromCategoryIDWithJoin(category_id, min_scrape_id)

    return jsonify(result), 200


@api_blueprint.route('/news_data/predicted_category',methods=['GET'])
def predicted_news_data_category():
    category_id = request.args.get("category_id")
    min_scrape_id = request.args.get("min_scrape_id")

    result = PredictedDataModel.getRecordFromCategoryIDWithJoin(category_id, min_scrape_id)

    return jsonify(result), 200


@api_blueprint.route('/categories',methods=['GET'])
def categories():
    categories = CategoryDataModel.getAllRecord()

    result = []

    for k in categories.keys():
        tmp = {}
        tmp["category_id"] = k
        tmp["category_name"] = categories[k]
        result.append(tmp)


    return jsonify(result), 200



@api_blueprint.route('/annotation', methods=['POST'])
def annotation():
    data = request.data
    data = json.loads(data)

    is_delete = data['is_delete']
    scrape_id = data['scrape_id']
    category = data['category']

    categories = CategoryDataModel.getAllRecord()

    keys = [k for k, v in categories.items() if v == category]

    if len(keys) != 1:
        return "category is wrong", 400
    category_id = keys[0]
    print("IS category_id  ", category_id)

    if is_delete == "true":
        TrainDataModel.delete(scrape_id, category_id)
        return "success", 200

    elif is_delete == "false":
        TrainDataModel.insert(scrape_id, category_id)
        return "success", 200
    
    return "invalid", 400
