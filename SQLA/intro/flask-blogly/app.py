"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)
db.create_all()
# Helper func
def form_data(data):
  '''Selects data from request form'''
  return request.form.get(data, '')
# User list 
@app.route('/users')
def user_list():
  '''Renders list of usrs'''
  Users = User.query.all();
  return render_template('users.html', users = Users)

# Home
@app.route('/')
def redirect_to_list():
  '''Redirects to list of Users'''
  return redirect('/users')

@app.route('/users/new')
def show_user_form():
  '''Show new User form'''
  return render_template('/user_form.html', action = 'Create', submit_route = '/users/new')

# add user
@app.route('/users/new', methods = ['POST'])
def add_new_user():
  '''Responds to new User form'''
  first_name = form_data('first_name')
  last_name = form_data('last_name')
  img_url = form_data('img_url')

  new_user = User(first_name = first_name, last_name=last_name, img_url = img_url)
  update_db(new_user)

  return redirect('/users')

# user details
@app.route('/users/<int:User_id>')
def show_user_details(User_id):
   '''Shows details about individual User'''
   user = User.query.get_or_404(User_id)
   return render_template('details.html', user=user)

# show edit page
@app.route('/users/<int:User_id>/edit')
def show_edit_form(User_id):
  '''Show new User form'''
  user = User.query.get_or_404(User_id)
  return render_template('/user_form.html', action = 'Edit', submit_route = '/user/<int:User_id>/edit')

# post user edit
@app.route('/users/<int:User_id>/edit', methods = ['POST'])
def edit_user(User_id):
  '''Responds to edit user form'''
  user = User.query.get_or_404(User_id)
  user.first_name = form_data('first_name')
  user.last_name = form_data('last_name')
  user.img_url = form_data('img_url')

  update_db(User)
  return redirect('/users')
  
  # Delete user 
@app.route('/users/<int:User_id>/delete', methods = ['POST'])
def delete_user(User_id):
  '''Deletes specified user'''
  user = User.query.get_or_404(User_id)
  db.session.delete(user)
  db.session.commit();
  return redirect('/users')