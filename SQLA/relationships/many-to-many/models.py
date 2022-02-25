from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

def update_db(data):
  db.session.add(data)
  db.session.commit()

  # MODELS GO HERE
    
class Department(db.Model):
    '''Department Model'''
    __tablename__ = 'departments'

    dept_code = db.Column(db.Text, primary_key=True)
    dept_name = db.Column(db.Text, nullable= False, unique=True)
    phone = db.Column(db.Text, default = '555-555-5555')

    def __repr__(self):
        return f"<Department {self.dept_code} {self.dept_name} {self.phone}>"
class Employee(db.Model):
    """Employee Model."""

    __tablename__ = "employees"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.Text, nullable=False, default='CA')    
    # # # # # # # # # # # # # # # ## # # # # 
    dept_code = db.Column(
        db.Text,
        db.ForeignKey('departments.dept_code'))

    # Setting backref gives department access to employee data
    dept = db.relationship('Department', backref='employees')
    assignments = db.relationship('EmployeeProject', backref='employee')
    projects = db.relationship('Project', secondary = 'employees_projects', backref = 'employees')
    # # # # # # # # # # # # # # # # # # # #
    def __repr__(self):
        return f"<Employee {self.name} {self.state} {self.dept_code} >"

class Project(db.Model):
  """Project Model."""

  __tablename__ = 'projects'

  proj_code = db.Column(db.Text, primary_key=True)
  proj_name = db.Column(db.Text, nullable= False, unique=True)
  assignments = db.relationship('EmployeeProject', backref='project')
# Ref table - THE MAGIC
class EmployeeProject(db.Model):
  """Employee Project Relation Model"""
  __tablename__ = 'employees_projects'
  
  emp_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
  proj_code = db.Column(db.Text, db.ForeignKey('projects.proj_code'), primary_key=True)
  role = db.Column(db.Text)





def get_dir():
  '''Show phone director: employee, department, and number'''
  # inefficient calls db for each emp
  emps = Employee.query.all();

  for emp in emps:
    if emp.dept is not None:
      print(emp.name, emp.dept.dept_code, emp.dept.phone)
    else:
      print(emp.name, '-','-')

def phone_dir_join():
  '''Show employess with join'''
  emps = (db.session.query(Employee.name,
                           Department.dept_name,
                           Department.phone)
          .join(Department).all())
  for name, dept, phone in emps:
    print(name,dept,phone)
