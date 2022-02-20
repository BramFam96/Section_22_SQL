from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


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
    # # # # # # # # # # # # # # # # # # # #
    def __repr__(self):
        return f"<Employee {self.name} {self.state} {self.dept_code} >"

def get_dir():
  '''Show phone director: employee, department, and number'''

  emps = Employee.query.all();

  for emp in emps:
    if emp.dept is not None:
      print(emp.name, emp.dept.dept_code, emp.dept.phone)
    else:
      print(emp.name, '-','-')
    
