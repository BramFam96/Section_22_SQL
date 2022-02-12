from flask import Flask, request, render_template, redirect, flash, session;
from flask_debugtoolbar import DebugToolbarExtension

# import flas-sqla
from flask_sqlalchemy import SQLAlchemy;


app = Flask(__name__)

################################# ALCHEMY ######################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///movies_example'
#We will get an error if we don't connect to a valid server;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
db = SQLAlchemy();
#NOTE Defines and initializes db connection:
db.app = app;
db.init_app(app);
################################################################################
# We run this file in ipython! #
################################################################################
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
  '''Renders homepage'''
  return render_template('home.html')