
from flask import Flask, render_template


def create_app():

  app = Flask(__name__, static_folder='./frontend/dist/static', template_folder='./frontend/dist')



  return app

app = create_app()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route("/test")
def index2():
    return "Hello testtetstteeee!!"


@app.route("/test2")
def index3():
    return "Hello 2222testtetstteeee!!"
if __name__ == "__main__":
    app.run()