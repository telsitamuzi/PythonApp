# APPlICATION FILE FOR 3155 PROJECT

import os  # os is used to get environment variables IP & PORT
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template
from flask import request

app = Flask(__name__)  # create an app

with app.app_context():


@app.route('/index')
def index():
    # to be implemented


@app.route('/login')
def login():
    # to be implemented


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)