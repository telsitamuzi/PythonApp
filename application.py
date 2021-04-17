# APPlICATION FILE FOR 3155 PROJECT

import os  # os is used to get environment variables IP & PORT
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from database import db


app = Flask(__name__)  # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app) # initializes database


with app.app_context():
    db.create_all()

@app.route('/index')
def index():
    # to be implemented


@app.route('/login')
def login():
    # to be implemented


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)