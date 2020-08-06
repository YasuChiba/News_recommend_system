
from flask import Flask


def create_app():

  app = Flask(__name__)


  return app

app = create_app()

@app.route("/")
def index():
    return "Hello World!!"


@app.route("/test")
def index2():
    return "Hello testtetstteeee!!"


@app.route("/test2")
def index3():
    return "Hello 2222testtetstteeee!!"
if __name__ == "__main__":
    app.run()