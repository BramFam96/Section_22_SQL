"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, delete_data, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)

#################################################### Helper func
def form_data(data):
  '''Selects data from request form'''
  return request.form.get(data, '')

#################################################################
############################ USER ROUTES
@app.route('/users')
def show_user_list():
  '''Renders list of all users'''
  users = User.query.order_by(User.last_name, User.first_name).all()
  return render_template('users/user-list.html', users = users)

########################################## G/P ROUTES FOR NEW USER 

@app.route('/users/new')
def show_user_form():
  '''Show new User form'''
  return render_template('users/form.html', action = 'Create', submit_route = '/users/new')

@app.route('/users/new', methods = ['POST'])
def post_user_form():
  '''Responds to new User form'''
  first_name = form_data('first_name')
  last_name = form_data('last_name')
  img_url = form_data('img_url')

  new_user = User(first_name = first_name, last_name=last_name, img_url = img_url)
  update_db(new_user)

  return redirect('/users')
######################################################################
################################################## Specific User Stuff
@app.route('/users/<int:user_id>')
def show_user_details(user_id):
   '''Shows details about individual User'''
   user = User.query.get_or_404(user_id)
   return render_template('users/view-user.html', user=user)

#################################################### G/P for user edit 
@app.route('/users/<int:user_id>/edit')
def show_user_edit_form(user_id):
  '''Show new User form'''
  user = User.query.get_or_404(user_id)
  return render_template('users/form.html', user = user, action = 'Edit', submit_route = '/user/<int:user_id>/edit')

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def post_user_edit_form(user_id):
  '''Responds to edit user form'''
  user = User.query.get_or_404(user_id)
  old_name = user.full_name;
  user.first_name = form_data('first_name')
  user.last_name = form_data('last_name')
  user.img_url = form_data('img_url')

  update_db(user)
  flash(f"Success! Changed {old_name}")
  return redirect(f'/users/{user_id}')
######################################################################  
  # Delete user 
@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
  '''Deletes specified user'''
  user = User.query.get_or_404(user_id)
  name = user.full_name
  delete_data(user)
  flash(f"User {name} has been deleted")  
  return redirect('/')
######################################################################
########################### POSTS 

#Show all posts
@app.route('/')
def show_home_page():
    """Show all posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)

# show specific post

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a page with info on a specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view-post.html', post=post)
#show new post form

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
  '''Show new post form'''
  user = User.query.get_or_404(user_id)
  tags = Tag.query.all();
  return render_template('posts/post-form.html', user=user, tags = tags, action='Add')


# show edit page for specific post

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show a form to edit an existing post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/post-form.html', post=post, tags=tags, action = 'Edit')

# POST ROUTES for post data
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_post_form(user_id):
    '''Submit new post'''
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=form_data('title'), content=form_data('content'), user=user, tags=tags)
    update_db(post);
    flash(f"Added '{post.title}' to {user.full_name}'s Posts")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_edit_post_form(post_id):
    """Handle form submission for updating an existing post"""
    post = Post.query.get_or_404(post_id)
    old_title = post.title;
    post.title = form_data('title')
    post.content = form_data('content')

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    update_db(post);
    flash(f'Successfully changed "{old_title}" to {post.title}')

    return redirect(f"/")
#####################################################################
#delete method
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    delete_data(post);
    
    flash(f'Post "{post.title}" has been deleted')

    return redirect(f"/users/{post.user_id}")
# TAGS ##############################################################
@app.route('/tags')
def show_tag_list():
  '''Shows list of all tags'''
  tags = Tag.query.all();
  return render_template('tags/list.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
  '''Shows posts associated with a tag'''
  tag = Tag.query.get_or_404(tag_id);
  return render_template('tags/view-tag.html', tag = tag)

# G/P New tag Form
@app.route('/tags/new')
def show_tag_form():
    '''Shows form for adding new tag'''
    return render_template('tags/form.html', action = 'Add')

@app.route('/tags/new', methods=['POST'])
def post_tag_form():
  '''Adds new tag to database'''
  name = form_data('name')
  tag = Tag(name=name)
  update_db(tag)
  return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_form_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/form.html', tag = tag, action = 'Edit')
  

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def post_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    old_name = tag.name;
    tag.name = form_data('name')
    update_db(tag)
    flash(f'Updated tag "{old_name}" to "{tag.name}"')
    return redirect(f'/tags/{tag.id}')
    
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    name = tag.name
    delete_data(tag);
    flash(f'Tag "{name}" has been deleted')
    return redirect('/tags')