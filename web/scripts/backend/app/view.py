from flask import Flask, render_template, request, Blueprint, current_app, jsonify
from .model.scrape_data_model import ScrapeDataModel

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/test',methods=['GET'])
def test():
  text = ScrapeDataModel.getLatestText()
  
  return text
  

@api_blueprint.route('/test2',methods=['GET'])
def test2():
  text = ScrapeDataModel.getRecord(5)
  
  return jsonify(text), 200
