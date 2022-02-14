"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

#   DB logic goes here
db = SQLAlchemy();

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
  img_url = db.Column(db.String(30), nullable = True)
  
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
  