from flask import Flask, render_template
from backend.app.view import api_blueprint
from backend.database import db, ma
from backend.config import Config


def create_app():

    app = Flask(__name__, static_folder='./frontend/dist/static', template_folder='./frontend/dist')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    app.config.from_object('backend.config.Config')
    db.init_app(app)
    ma.init_app(app)

    return app

app = create_app()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route("/api/test")
def index2():
    
    return "Hello testtetstteeee!!"



@app.route("/test2")
def index3():
    return "Hello 2222testtetstteeee!!"

if __name__ == "__main__":
    app.run()