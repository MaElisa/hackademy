# run with         python -m flask run

from flask import Flask,render_template,Response
app = Flask(__name__)

@app.route("/")
def home():
  return render_template("")