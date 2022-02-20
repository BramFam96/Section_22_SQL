"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)

# Helper func
def form_data(data):
  '''Selects data from request form'''
  return request.form.get(data, '')

# Root
@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/home.html", posts=posts)

##############################################################
# USER ROUTES
# User list 
@app.route('/users')
def user_list():
  '''Renders list of usrs'''
  users = User.query.order_by(User.last_name, User.first_name).all()
  return render_template('users/user-list.html', users = users)


@app.route('/users/new')
def show_user_form():
  '''Show new User form'''
  return render_template('users/form.html', action = 'Create', submit_route = '/users/new')

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
@app.route('/users/<int:user_id>')
def show_user_details(user_id):
   '''Shows details about individual User'''
   user = User.query.get_or_404(user_id)
   return render_template('users/view-user.html', user=user)

# show edit page
@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
  '''Show new User form'''
  user = User.query.get_or_404(user_id)
  return render_template('users/form.html', action = 'Edit', submit_route = '/user/<int:user_id>/edit')

# Edit user
@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
  '''Responds to edit user form'''
  user = User.query.get_or_404(user_id)
  user.first_name = form_data('first_name')
  user.last_name = form_data('last_name')
  user.img_url = form_data('img_url')

  update_db(User)
  return redirect('/users')
  
  # Delete user 
@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
  '''Deletes specified user'''
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit();
  return redirect('/users')
##############################################################
# POST ROUTES

#New posts
@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
  '''Show new post form'''
  user = User.query.get_or_404(user_id)
  return render_template('posts/post-form.html', user=user, action='Add')

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    '''Submit new post'''
    user = User.query.get_or_404(user_id)
    post = Post(title=request.form['title'], content=request.form['content'], user_id=user)
    update_db(post);
    flash(f"Added {post.title} to {user.full_name}'s Posts")
    return redirect(f"/users/{user_id}")

# View posts
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/view-post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/post-form.html', post=post, action = 'Edit')


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    update_db(post);
    flash(f"Successfully edited '{post.title}'")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    update_db(post)
    flash(f"Deleted '{post.title}'")

    return redirect(f"/users/{post.user_id}")