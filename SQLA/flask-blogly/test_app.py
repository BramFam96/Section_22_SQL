from unittest import TestCase

from app import app
from models import db, User, Post, update_db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class ViewFuncTests(TestCase):
    """Tests blogly apps view functions."""

    def setUp(self):
        """Add sample User."""

        db.session.rollback()
        # Create a single user for each test:
        user = User(first_name="TestUser", last_name="TestUser")
        update_db(user)
        # commiting generates an id but this obj is not yet associated with it
        # bind id to self
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        

    def test_user_list(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Create', html)
    
    def test_show_user_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h2 class = 'mt-2'>Posts</h2>", html)
    
    def test_show_edit_form(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit', html)
# Test user post route
    def test_add_user(self):
        with app.test_client() as client:
            u = {"first_name": "TestUser2", "last_name": "TestUser2"}

            res = client.post("/users/new", data=u, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser2", html)
# Testing posts
    def test_root(self):
        with app.test_client() as client:
            post = Post( title ='test',  content = 'test_content', user_id = self.user_id)
            update_db(post)
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('test', html)
            self.assertIn('test_content', html)
            
    def test_show_new_post_form(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/posts/new') 
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('col-form-label">Title</label>', html)
    
    def test_add_new_post(self):
        with app.test_client() as client:
            post = {"title": "Test title", "content": "Test content", "user_id":f'{self.user_id}'}
            res = client.post(f"/users/{self.user_id}/posts/new", data=post, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test title", html)
# Testing posts

# @app.route('/users/<int:user_id/posts/new')
# def show_new_post_form(user_id):
#   '''Show new post form'''
#   user = User.query.get_or_404(user_id)
#   return render_template('posts/post-form.html', user=user, action='Add')
