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

- [Set up](#set-up)
- [DB and Model](#connecting-db-and-model)
- [Populating DB](#creating-new-data)
- [Querying](#query-basics)

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

```
<!-- In our console -->
ipython

%run file.py

<!-- Run execute once  -->

movies = db.session.execute("SELECT * FROM movies")
list(movies)

<!-- Unfortunately this is a tuple. -->
```

Instead, we will use python to structure this data into dicts

# File structure

We've been writing this in a single, [boilerplate](boiler_unformatted.py) file.

This is unrealistic. Consider that SQLA allows us to write things like:

```
class Example:
test = Example(title='test', count = 1)
test.title = 'new_test'

test.runSomething()
```

Which is Equivalent to:

```
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

```
<!-- In the terminal -->

createdb pet_shop_db

<!-- In app.py -->

Modify DATABASE_URL to point to new db
```

## **Structuring the python model**

---

### **Check model section of [models](boilerplate/app.py)**

---

## **Seeding db from [python model](boilerplate/models.py)**

---

```
<!-- In the terminal -->
ipython

%run app.py
<!-- Again we only want to initialize a table once -->
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

###**Using our Model**

---

We need to import specific models along with db and session in [app](boilerplate/app.py)

&nbsp;

### [back to top](#table-of-contents)

# Creating new data

1. ### **Create a new instance we wish to save**

---

```
<!-- In the terminal -->

ipython
%run app.py
Pet

<!-- returns models.Pet -->

newPet = Pet(name='Jack', species = 'dog', hunger = 20)

newPet
<!-- returns useless <Pet (transient <int_seq>)> -->
<!-- We will correct this with a __repr__ class method -->
dir(newPet)
```

This **will not** update the db itself!  
We still need to _add_ and _commit_ these changes

2. ### **Add data to db**

---

```

<!-- Could wrap in a func called commit -->

db.session.add(newPet);
db.session.commit()

<!-- Just like git, we can add many changes and commit them at once -->

newPet

<!-- Retuns <Pet 1> -->

dir(db.session)
```

## **Adding multiple objs to db**

---

```
pet_names = ['Brock', 'Rocket', 'Scout', 'Brian'];
species = ['gecko', 'cat', 'sparrow', 'dog'];

<!-- zip(name, species) will create a compressed iterable -->
<!-- We put this inside a list comprehension -->

pets = [Pet(name = n, species = s) for n,s in zip(names,species)]

<!-- pets[0].name = 'Brock' pets[0].species = 'gecko' -->

db.session.add_all(pets);

```

## **Error handling and Rollbacks**

---

In our db model we have set name to be a unique value  
If we violate this:

```
dog = Pet(name='Rocket', species='dog')
db.session.add(dog)
db.session.commit();
<!-- Error! -->
```

Obviously, we will get a db error  
Less obvious however, is that this problem data still exists in our session  
**valid commits will stop working**

```
db.session.add(unique_pet)
db.commit()
<!-- Invalid req error: transaction has been rolled back -->
```

We need to remove rocket the dog from our db session:

```
db.session.rollback();
db.session.add(unique_pet)
db.commit()
<!-- Success! -->
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
   <!-- query return shows UPDATE call -->

&nbsp;

### [back to top](#table-of-contents)

# Query fundamentals

So far we've been creating/updating some instance and syncing it to our db

&nbsp;

_Query is a bit different_  
Each obj we instantiate has a built in query and query_class attribute

```
**dir(Pet.query)**
<!-- Reveals the many methods query includes -->
```

_Important_ querying is a two step process, like updating

## Query Basics

---

## Formatting Queries

### **Syntax**

```
Pet.query() = SELECT * FROM pet, but does not initialize without specificity
```

The specificity requirements is literally a WHERE statement  
We can perform the simplest query by specifying all:

```
Pet.query.all() return SELECT * FROM pet
```

### **Query for a single value**

```
Pet.query.get(3)
<!--defaults to PK, which is id, returns pet where id = 3 -->
```

### **Filtered Queries**

```
Pet.query.filter_by(species='cat')
<!--This does not execute the query-->
```

We need to chain .all(), or another WHERE call:

```
Pet.query.filter_by(species='cat').all()
```

If we pass multiple conditions into filter_by they are turned into AND statements  
Works well with specific values- but won't work for conditions and, or, less than etc;

&nbsp;

### [back to top](#table-of-contents)
