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
class Pet(db.Model):
  '''Pet Model'''
  # Set-up
  __tablename__ = 'pets'
  
  def __repr__ (self):
    '''Show pet info'''
    s = self;
    return f'''<Pet id={s.id} name='{s.name}' species='{s.species}' hunger={s.hunger}>'''
  # class method example
  @classmethod
  def get_by_species(cls, species):
    return cls.query.filter_by(species=species).all();
  # Colum structure
  id = db.Column(db.Integer, primary_key= True, autoincrement = True)
  name = db.Column(db.String(50), nullable = False, unique = True)
  species = db.Column(db.String(30), nullable = True)
  hunger = db.Column(db.Integer, nullable = True, default = 20)
  # Methods
  def greet(self):
   return f'Hi, I am {self.name} the {self.species}!'

  def feed(self, amt=20):
   '''Update pet hunger'''
   self.hunger -=amt
   self.hunger = max(self.hunger, 0)
   update_db(self);
  