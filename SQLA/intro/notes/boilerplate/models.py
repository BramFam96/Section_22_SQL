from flask_sqlalchemy import SQLAlchemy

#   DB logic goes here
db = SQLAlchemy();
#Best practice:
def connect_db(app):
  db.app = app;
  db.init_app(app);

#    MODELS GO HERE     #
 
class Pet(db.Model):
  '''Pet Model'''
  def __repr__ (self):
    '''Show pet info'''
    s = self;
    return f'<Pet id = {s.id} name = {s.name} species = {s.species} hunger = {s.hunger}>'
  # Create table
  __tablename__ = 'pets'
  #define columns
  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  name = db.Column(db.String(50), nullable = False, unique = True)
  species = db.Column(db.String(30), nullable = True)
  hunger = db.Column(db.Integer, nullable = True, default = 20)
  
  