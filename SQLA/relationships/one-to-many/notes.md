# One to many associations

## Table of Contents

---

## Goals

---

- Translate relationships between tables to relationships between Python classes
- Deeper dive into SQLAlchemy querying
- Compare different approaches to querying in SQLAlchemy

## Example

---

We have two databases:

1. **departments** -> dept_code[PK], dept_name, phone
2. **employees** -> id, name, state, dept_code[FK]

## Start up

We have two models and have imported connect_app(db) into app.py;

Let's start up our databases!

```py
%run app.py
db.create_all();
# Equivalent

```

employees_db now contains our two tables!

## Adding data

---

Let's add some data

```py
d = Department(dept_code='hr', dept_name ='Human Resources', phone = 555-555-5555)
db.session.add(d)
db.session.commit()
```

## FK constraints

---

```py
# in out employee model
    dept_code = db.Column(
        db.Text,
        db.ForeignKey('departments.dept_code'))
```

We're going to see an **additional layer** we can add on top

## Update -revisited

Once we update our model we should reset our db

```SQL
ipython
%run app.py
db.drop_all()
db.create_all()
```

Follow steps in [Adding data](#adding-data)  
_Note_ we need to add a dept for an employee to belong to;

## Seed file

---

It's annoying dropping and adding our tables when we change model structure  
Instead, we **make** a _seed file_
See [Seed](seed.py)  
Now we can easily reset our tables!

## Relationship method

---

db.relationship() is a powerful method that gives individual objects  
access to corresponding data from other tables

```py
dept = db.relationship('Department');
```

This data **will not** make a new column!
It **will** allow us to access dept info from a specific employee
_without joining_

### Accessing relational data

```SQL
%run app.py

emp = Employee.query.get(1);
emp.name -> 'River Bottom'
emp.dept -> departments __repr__ function;
emp.dept.dept_name -> Marketing
```

When we ask for emp.dept SQL runs a JOIN for us!  
This works both ways (_if we include backrefs_):

```SQL
dep = Department.query.get('mktg')
for emp in dep.employees:
  print(emp.name)
```

## backrefs

To get the functionality above we need to make relationships in each of our models  
Looking at [models](models.py) we instead wrote _one relationship_ on employee;

```py
dept = db.relationship('Department', backref='employees')
```

## Using Relationships

Goal: Make a phone directory:

- Show directory of employees with department and phone number:

```py
In models:
def phone_dir():
  '''Show phone director: employee, department, and number'''

  emps = Employee.query.all();

  for emp in emps:
    if emp.debt is not None:
      print(emp.name, emp.dept.dept_code, emp.dept.phone)
    else:
      print(emp.name, '-','-')
```

**Don't forge to import into app.py!**  
Our output is somewhat illegible. This is b/c we have echo enable on line 8 of [app](app.py)

```py
app.config['SQLALCHEMY_ECHO'] = False;
```

Also this process is incredibly inefficient!

### Routing

We're going to build the phone_dir funcitonality in our routing;
Check [app](app.py) and [phones.html](templates/phones.html)

## More Queries

---

### Chaining queries

Recall:

```py
Employee.query.filter(Employee.id > 1) -> does not send a query w/o .all() or .first();
```

This allows us to chain queries:

```py
*new_emps* = Employee.query.filter(Employee.id > 1)
new_ca_emps = *new_emps*.filter(Employee.state == 'CA')
new_ca_emps.all() <- triggers query
```

### Flexible Select (tuples)

So far we have been our queries have been _SELECT (_)\*
We can instead get specific values, like names only  
**New syntax**

```py
db.session.query(Employee.id, Employee.name).all();
Returns a list of tuples! -> no useful object methods
```

This is equivalent to _SELECT id, name FROM employees_  
Useful when:

- We **don't** need full SQLA objets/all field
- We don't have object to update
- Can't call useful methods on objects
  - BONUS! It's a bit faster

### Fetching method recap

- .all()
- .first()
- .one()
- .one_or_none()
- .count()

```py
Employee.query.filter_by(state='CA').count()
```

## Common operators

SQL operators:

- WHERE ... OR
- WHERE ... AND
- WHERE ... IN (item1, item2, item3)

```py
q = Employee.query
# Normal Py operators
q.filter(Employee.name == 'Jane')
q.filter(Employee.name != 'Jane')
q.filter(Employee.id > 5)
# SQL Equivalents
q.filter(Employee.name.like('%Jan%')) # LIKE/ILIKE
# % is a wildcard, we can use - for exact length matches like state.like('C-)'
q.filter(Employee.id.in_([22,33,44])) # IN ()
q.filter(Employee.state == 'CA', Employee.id > 65) #AND -> ','
q.filter((Employee.state == 'CA') | (Employee.id > 65)) #OR -> '|'
NOTE the OR syntax can be used with & operator for AND comparisons
q.group_by('state').having(db.func.count(Employee.id) > 2)
q.order_by('id')
q.offset(10)
q.limit(10)
See querydocs!
```
