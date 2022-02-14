from flask import Flask, request, render_template, redirect, flash, session;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, Pet

app = Flask(__name__)

################################# CONFIG W/ ALCHEMY  ######################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
##################################  HELPFUL DEV DEBUG ##############################
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)

#From models.py
connect_db(app)

# Helper func
def form_data(data):
  '''Selects data from request form'''
  return request.form[data]

#Home get request 
@app.route('/')
def list_pets():
  '''Renders list of pets'''
  pets = Pet.query.all();
  return render_template('list.html', pets = pets)

#Home create post request
@app.route('/', methods = ['POST'])
def add_new_pet():
  '''Responds to new pet form'''
  name = form_data('name')
  species = form_data('species')
  hunger = form_data('hunger')
  hunger =  int(hunger) if hunger else None

  new_pet = Pet(name=name,species=species, hunger = hunger)

  # Update db
  update_db(new_pet)

  # Redirect to details, we could choose '/'
  return redirect(f'/{new_pet.id}')


@app.route('/<int:pet_id>')
def show_pet_details(pet_id):
   '''Shows details about individual pet'''
   pet = Pet.query.get_or_404(pet_id)
   return render_template('detail.html', pet=pet)
   
@app.route('/species/<species_id>')
def show_pets_by_species(species_id):
  specie = Pet.get_by_species(species_id)
  return render_template('species.html', species = species_id, specie = specie)