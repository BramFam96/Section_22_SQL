from models import User, Post, Tag, PostTag, db, update_db
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

update_db(users)

# Add Posts
first = Post(title = 'First Post!', content = 'Howdy there!', user_id = 2)
second = Post(title = 'Another one!', content = "We're back!!", user_id = 2)
third = Post(title = 'Greetings!', content = "New here", user_id = 1)

# Add tags
happy = Tag(name = 'Happy')
mad = Tag(name = 'Mad')
sad = Tag(name = 'Sad')
excited = Tag(name='Excited')

tags = [happy,mad,sad,excited]

update_db(tags)

first.tags.append(happy)
second.tags.append(excited)
third.tags.append(mad)

posts = [first,second, third];

update_db(posts)