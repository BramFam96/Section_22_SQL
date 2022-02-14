# Overview

Whenever connecting any codebase to a database we will download a specific package  
For our use-case we will be using **SQLAlchemy** to connect _flask_ and _postgres_

- **SQLA** is an _ORM_ (object-relational mapper)
- It can be used by itself, but is best used to translate code into relational dbs;
- Initializing packages
  - pip install psycopg2-binary
  - pip install flask-sqlalchemy (specific flavor of SQLA)

# Goals

Learn to use **OO techniques** with relational DBs

-No more writing SQL code ourselves!
-Replace our chonky strings with neat class methods!

# Table of Contents

- Basics of working with model, creation, connection, queries, additions, updates
  - [Set up](#set-up)
  - [DB and Model Intro](#db-and-model)
  - [Populating DB](#creating-new-data)
  - [Querying](#query-basics)
  - [Model Methods](#model-methods)
- Combining SQLA with flask
  - [Adding routes and UI](#integrating-flask)

# Set up

To get up and running we need to connect to a DB and import flask-sqlalchemy

```
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
...
db = SQLAlchemy();
db.app = app;
db.init_app(app);
```

We typically seperate db logic from view funcs, but for this example check:

## **[simple_app](boiler_unformatted.py)**

---

## Viewing data

---

```sql
--- In our console
ipython

%run file.py

--- Run execute once

movies = db.session.execute("SELECT * FROM movies")
list(movies)

--- Unfortunately this is a tuple.
```

Instead, we will use python to structure this data into dicts

# File structure

We've been writing this in a single, [boilerplate](boiler_unformatted.py) file.

This is unrealistic. Consider that SQLA allows us to write things like:

```py
class Example:
test = Example(title='test', count = 1)
test.title = 'new_test'

test.runSomething()
```

Which is Equivalent to:

```SQL
INSERT INTO EXAMPLE (title, count)
VALUES
('...','...')
```

This straight forward syntax is easier, and indeed, the whole point of **ORMS**  
We accomplish this by **building models** to talk to our db behind the scenes.  
These models can become chunky, and so it make sense to seperate them from our main file.
Check the structure of the local 'boilerplate' folder.

&nbsp;

### [back to top](#table-of-contents)

# **DB and Model**

When we create a model we are mirroring an equivalent db table

**First we need to create and connect to sql db**

```SQL
--- In the terminal

createdb pet_shop_db

--- In app.py

Modify DATABASE_URL to point to new db
```

## **Structuring the python model**

---

### **Check model section of [models](boilerplate/app.py)**

---

## **Seeding db from [python model](boilerplate/models.py)**

---

```sql
--- In the terminal
ipython

%run app.py
--- Again we only want to initialize a table once
db.create_all()

Output:
CREATE TABLE pets (
  id SERIAL NOT NULL,
  name VARCHAR(50) NOT NULL,
  species VARCHAR(30),
  hunger INTEGER,
  PRIMARY KEY (id),
  UNIQUE (name)
)
```

### **Updating our Model**

---

We need to _**DROP TABLE** table_ in psql before changing our models

### **Using our Model**

---

We need to import specific models along with db and session in [app](boilerplate/app.py)

&nbsp;

### [back to top](#table-of-contents)

# Creating new data

1. ### **Create a new instance we wish to save**

---

```sql
--- In the terminal

ipython
%run app.py
Pet

--- returns models.Pet

newPet = Pet(name='Jack', species = 'dog', hunger = 20)

newPet
--- returns useless <Pet (transient <int_seq>)>
--- We will correct this with a __repr__ class method
dir(newPet)
```

This **will not** update the db itself!  
We still need to _add_ and _commit_ these changes

2. ### **Add data to db**

---

```sql

--- Could wrap in a func called commit

db.session.add(newPet);
db.session.commit()

--- Just like git, we can add many changes and commit them at once

newPet

--- Retuns <Pet 1>

dir(db.session)
```

## **Adding multiple objs to db**

---

```sql
pet_names = ['Brock', 'Rocket', 'Scout', 'Brian'];
species = ['gecko', 'cat', 'sparrow', 'dog'];

--- zip(name, species) will create a compressed iterable
--- We put this inside a list comprehension

pets = [Pet(name = n, species = s) for n,s in zip(names,species)]

--- pets[0].name = 'Brock' pets[0].species = 'gecko'

db.session.add_all(pets);

```

## **Error handling and Rollbacks**

---

In our db model we have set name to be a unique value  
If we violate this:

```sql
dog = Pet(name='Rocket', species='dog')
db.session.add(dog)
db.session.commit();
--- Error!
```

Obviously, we will get a db error  
Less obvious however, is that this problem data still exists in our session  
**valid commits will stop working**

```sql
db.session.add(unique_pet)
db.commit()
--- Invalid req error: transaction has been rolled back
```

We need to remove rocket the dog from our db session:

```sql
db.session.rollback();
db.session.add(unique_pet)
db.commit()
--- Success!
```

## **Modifying a pet**

---

1. Select the thing we want to modify in Py
   - Not as useful since we are working in one terminal and still have access
   - We will learn this later
2. Change particular values;
   - jack.name = 'dash'
3. Update db
   - db.session.add(jack)
   - db.commit();
     --- query return shows UPDATE call

&nbsp;

### [back to top](#table-of-contents)

# Query fundamentals

So far we've been creating/updating some instance and syncing it to our db

&nbsp;

_Query is a bit different_  
Each obj we instantiate has a built in query and query_class attribute

```sql
**dir(Pet.query)**
--- Reveals the many methods query includes
```

_Important_ querying is a two step process, like updating

## Query Basics

---

## Formatting Queries

### **Syntax**

```sql
Pet.query() = SELECT * FROM pet, but does not initialize without specificity
```

The specificity requirements is literally a WHERE statement  
We can perform the simplest query by specifying all:

```sql
Pet.query.all() return SELECT * FROM pet
```

### **Query for a single value**

```py
Pet.query.get(3)
---defaults to PK, which is id, returns pet where id = 3
```

### **Filter Queries**

1. filter_by

```sql
Pet.query.filter_by(species='cat')
---fliter_by does not execute a query
```

We need to chain .all(), or another WHERE value:

- get(pk)
- all()
- first()
- one()
  - if no record is found we get an err. if records > 1 err;
- one_or_none()
  - Get first record error if records > 1

```sql
Pet.query.filter_by(species='cat').all()
```

If we pass multiple conditions into filter_by they are turned into AND statements

Doesn't work for conditions like and, or, between etc;

1. filter  
   filter is capable of more complex conditions, but has a more explicit syntax

```sql
Pet.query.filter(Pet.species == 'dog').all()
--- NOTE Pet.species AND double '=='
```

Typically, '==' operations result in a T/F statement

It's used here b/c SQLA has changed its default behavior on columns

```sql
Pet.species == 'cat' -> returns a Binary Expression, not T/F
```

How the default method is changed

```sql
dir(Model.column) -> reveals its dunder methods;
-- One of these methods are __eq__

help(Pet.name.__eq__)
-- Reveals its been modified to produce a SQL compliant clause
-- This modification has also been made to !=, <, >
```

Let's try an actual query:

```sql
ipython
%run boilerplate/app.py

Pet.query.filter(Pet.hunger < 50, Pet.species =='dog').all();
```

We'll learn how to use other operators, or, like, ilike, between, in, etc;

&nbsp;

### [back to top](#table-of-contents)

# Model Methods

Just like the **repr** method we can add custom methods on our models

## Simple method

To create a new method we simply add it to the [Model file](boilerplate/models.py):

```py
def greet(self):
   return f'Hi, I am {self.name} the {self.species}!'
```

We **do not** need to do anything else to use this method

```sql
ipython
%run boilerplate/app.py

test = Pet.query.get(1);
test.greet()
-- Output: 'Hi, I am Jack the dog!'
```

Good time to look at calling a method on all objs:

```sql
all_pets = Pet.query.all();
for p in all_pets:
   print(p.greet());
```

## Methods that update!

---

We make a method called feed to update pet hunger  
We want this to be updated in our model **and** db

```py
def feed(self, amt=20):
   '''Update pet hunger'''
   # Updates local value
   self.hunger -=amt
   self.hunger = max(self.hunger, 0)
   # Update SQL db
   db.session.add(self)
   db.session.commit()
```

## Class Methods

---

Reminder class methods interact with the class, **not** individual instances
Therefor they are passed _cls_ and **not** _self_  
Examples include

- get hungry pets
- feed all pets
- selecting by species
- _query_

```py
@classmethod
def get_by_species(cls, species):
   return cls.query.filter_by(species=species).all();
```

One more example

```py
@classmethod
def get_all_hungry(cls,species):
   return cls.query.filter(Pet.hunger>10).all();
```

&nbsp;

### [back to top](#table-of-contents)

# Integrating Flask

## Flask-SQLAlchemy

---

We've been using flask-sqlaclhemy for a reason!  
It makes it easy for us to

- Tie SQLAlchemy session to our flask respone
- find things in SQLAlc's API
- query on model's themselves(SQLA doesn't do this normally)

Lets use flask to render our data and create a form for new pets

## Routes

Rendering our data as a list:

```py
# In boilerplate/app.py

@app.route('/')
def list_pets():
  '''Renders list of pets'''

  pets = Pet.query.all();
  return render_template('list.html', pets = pets)
```

We should structure this as a list and details page;  
We'll want a route like /{id} to return a specific pet's data

```py
# In boilerplate/app.py
@app.route('/<int:pet_id>')
def show_pet_details():
   '''Shows details about individual pet'''
   pet = Pet.query.get(pet_id)
   return render_template('details', pet=pet)
```

This will err if we get ids greater than len + 1!  
Introducing _get_or_404()_

```py
pet = Pet.query.get_or_404(pet_id)
```

## Advanced Routing

---

We want users to see all pets of a particular species  
by clicking a link or button from individual detail pages  
_We have already made the cls method get_by_species_

1. Create a new route:
   ```py
   <!-- species id is a string like 'cat' or 'dog' -->
   @app.route('/species/<species_id>'):
      def show_pets_by_species(species_id):
         specie = Pet.get_by_species(species_id)
         return render_template('species.html', species = species_id, specie = specie)
   ```

## Creating things

---

We have a form on our homepage  
Let's create a post route at home to handle this form:

```py
@app.route('/',methods=['POST'])
def add_pet():
   '''Adds pet to db'''

```

## Deleting things

---

Incredibly straight forward

Remember

```py
Pet.query.filter_by(hunger=0)
# does not execute without call method;
```

.delete() is a call method we can add to any select

```py
Pet.query.get(2).delete()
```

Once we delete a pet the change is reflected in local state  
_we still need to run **db.session.commit()** to change the db state!_

## Undo delete

---

db.session.rollback()

- works as long as we haven't commited!

## Seeding db

---

Seeding is very similar to psql without flask.  
Structural **difference**

- python syntax!
- seed should import model and db from models and app from app
- db.drop_all() / db.create_all() replace sql commands
- Model.query.delete() replaces drop tables
- data is session.add()'d and session.commit()'d
  We run this file with **python file-path**  
   Reference: [seed file](boilerplate/seed.py)

## Testing

---

We create a seperate file for testing models and app routes

- import model and db into both of these routes!
  We create a new db to prevent mucking up the real db

```py
# in our console
createdb pet_shop_test;
# in both test_flask and test_model files:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
```

Reference: [Model tests](boilerplate/test_models.py) and [App test](boilerplate/test_app.py)

The built in testing module gets tripped up when our files are buried too deep.  
Remember we can run unittest from the console!

```sql
python -m unittest test_models.py
```

&nbsp;

### [back to top](#table-of-contents)
