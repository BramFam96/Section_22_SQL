from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
whiskey = User(first_name='Whiskey', last_name = 'Tango')
bowser = User(first_name='King', last_name = 'Bowser')
spike = User(first_name='Spike', last_name = 'Unknown')

users = [whiskey,bowser,spike];
# Add new objects to session, so they'll persist
for user in users:
  db.session.add(user)

# Commit--otherwise, this never gets saved!
db.session.commit()
