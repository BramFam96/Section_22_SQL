# Goals

- Make explicit joins with SQLAlchemy
- Work with many-to-many relationships

## Joins

---

Joins can be an efficient alternative to for loops

- More explicit about what to get
- Connects tables without defined relationships
- Needed for outer joins

### Syntax

```py
def get_dir_join():
  '''Show employess with join'''
  emps = (db.session.query(Employee.name, Department.phone).join(Deparment).all())
  # this could be filter, first, etc;
  for name, dept, phone in emps:
    print(name,phone)
```

.join(cls) is critical or we'll get a garbage cross-join  
this is an _inner join_

- employees with no dept will not be returned
  if we access to all attributes and methods we can join the classes themselves:

```py
def get_dir_join_class():
  emps = (db.session.query(Employee,Department).join(Department).all())
    # gets a list of class tuples
  for emp, dept in emps:
    print(emp.name,dept.dept_name,dept.phone)

```

## Outer joins

To make an outer join we call .outerjoin instead of .join

```SQL
db.session.query(Employee.name, Department.phone).outerjoin(Deparment).all()

-- Reversing the syntax would reveal deps without employees
```

*Outer-joins* Employee and Department -> emps with no dep are returned;

# Many-to-many Relationships

Many-to-many relationships neccesitate a third db that tracks their PK's
