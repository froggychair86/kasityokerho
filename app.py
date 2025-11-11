from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tässä voi suunnitella käsityökerhon tapaamisia."
