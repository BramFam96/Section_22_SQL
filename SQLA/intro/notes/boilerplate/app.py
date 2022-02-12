from flask import Flask, request, render_template, redirect, flash, session;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)

################################# CONFIG W/ ALCHEMY  ######################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
##################################  HELPFUL DEV DEBUG ##############################
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)

#From models.py
connect_db(app)

#Check connection;
#movies = db.session.execute('SELECT FROM moves')

@app.route('/')
def home_page():
  '''Renders homepage'''
  return render_template('home.html')