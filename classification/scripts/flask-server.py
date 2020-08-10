from flask import Flask
import subprocess


app = Flask(__name__)

classification_process = None

@app.route('/train_and_predict')
def train_and_predict():
    global classification_process
    if classification_process is not None:
        if classification_process.poll() is None:
            return "now processing", 102
        
    classification_process = subprocess.Popen(['python3', '/root/classification/scripts/main.py'], shell=False)    
    return "success", 200

@app.route('/')
def test():

    return "teeeeest"


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)