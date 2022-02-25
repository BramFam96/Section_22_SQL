"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

#   DB logic goes here
db = SQLAlchemy();

# Default img url
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

#Best practice:
def connect_db(app):
  db.app = app;
  db.init_app(app);

# Update single changes:
def update_db(data):
  if type(data) is list:
    db.session.add_all(data);
    db.session.commit();
  else:
    db.session.add(data);
    db.session.commit();

def delete_data(data):
  db.session.delete(data);
  db.session.commit();

#    MODELS GO HERE     #
class User(db.Model):
  '''User Model'''
  # Set-up
  __tablename__ = 'users'
  
  def __repr__ (self):
    '''Show user info'''
    s = self;
    return f'''<User id={s.id} first_name='{s.first_name}' last_name='{s.last_name}' img_url='{s.img_url}'>'''

  # Colum structure
  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  first_name = db.Column(db.String(50), nullable = False)
  last_name = db.Column(db.String(50), nullable = False)
  img_url = db.Column(db.String(250), nullable = True, default=DEFAULT_IMAGE_URL)

  posts = db.relationship("Post", backref='user', single_parent = True, cascade="all, delete-orphan")
  @property 
  def full_name(s):
    '''Show full name'''
    return f"{s.first_name} {s.last_name}"


class Post(db.Model):
  '''Post Model'''
  __tablename__ = 'posts'
  def __repr__(self):
    '''Show post structure'''
    s = self
    return f'''
    Post {s.id}: '{s.title}' 
    created_at={s.created_at}
    '{s.content}' '''

  #Column structure
  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  title = db.Column(db.Text, nullable = False)
  content = db.Column(db.String(200), nullable = False)
  created_at = db.Column(db.DateTime, nullable= False,
                         default = datetime.datetime.now)
  user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))
    # Link posts
  
  
  @property
  def friendly_date(self):
    """Return nicely-formatted date."""
    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
  '''Tag model'''

  __tablename__ = 'tags'
  def __repr__(self):
    s = self
    return f'''<Tag id = {s.id} name = {s.name}'''

  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  name = db.Column(db.Text, unique = True, nullable = False)
  posts = db.relationship('Post', secondary = 'posts_tags', backref = 'tags', cascade='all,delete')

class PostTag(db.Model):
  """Post Tag ref table"""
  
  __tablename__ = 'posts_tags'
  
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
  # # class method example
  # @classmethod
  # def get_by_species(cls, species):
  #   return cls.query.filter_by(species=species).all();
    

  