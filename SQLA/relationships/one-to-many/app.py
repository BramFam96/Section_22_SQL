from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Employee, Department, get_dir

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)

# Routing goes here
@app.route('/phones')
def list_directory():
  emps = Employee.query.all();
  return render_template('phones.html', emps=emps)
