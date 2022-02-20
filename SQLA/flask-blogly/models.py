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
  db.session.add(data);
  db.session.commit();
#    MODELS GO HERE     #
class User(db.Model):
  '''User Model'''
  # Set-up
  __tablename__ = 'users'
  
  def __repr__ (self):
    '''Show user info'''
    s = self;
    return f'''<User id={s.id} first name='{s.first_name}' last name='{s.last_name}' img url='{s.img_url}'>'''

  # Colum structure
  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  first_name = db.Column(db.String(50), nullable = False)
  last_name = db.Column(db.String(50), nullable = False)
  img_url = db.Column(db.String(250), nullable = True, default=DEFAULT_IMAGE_URL)
  # Link posts
  posts = db.relationship("Post", backref='users', cascade="all, delete-orphan")
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
  @property
  def friendly_date(self):
    """Return nicely-formatted date."""
    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

  # # class method example
  # @classmethod
  # def get_by_species(cls, species):
  #   return cls.query.filter_by(species=species).all();
    
  # # Methods
  # def greet(self):
  #  return f'Hi, I am {self.name} the {self.species}!'

  # def feed(self, amt=20):
  #  '''Update pet hunger'''
  #  self.hunger -=amt
  #  self.hunger = max(self.hunger, 0)
  #  update_db(self);
  