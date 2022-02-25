from unittest import TestCase

from app import app
from models import db, User, Post, Tag, update_db

# SET-UP
###################################################################################

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

########################################################################################

class ViewFuncTests(TestCase):
    """Tests blogly apps view functions."""

# CONFIG
########################################################################################
    @classmethod 
    def setUpClass(cls):
        tag = Tag(name='tag')
        update_db(tag)
        super(ViewFuncTests, cls).setUpClass()
        cls.tag_id = tag.id;


    def setUp(self):
        """Add sample User."""

        # Create a single user for each test:
        user = User(first_name="Test", last_name="User")
        update_db(user)        
        # commiting generates an id but this obj is not yet associated with it
        # bind id to self
        self.user_id = user.id
        
        post = Post( title ='test',  content = 'test_content', user_id = self.user_id)
        
        update_db(post)
        self.post_id = post.id
        

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

# Get routes for user        
########################################################################################

    def test_show_user_list(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/users/1">Test User</a>', html)

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
            self.assertIn("Posts</h2>", html)
    
    def test_show_user_edit_form(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit', html)


# POST ROUTES FOR USER
########################################################################################

    def test_post_user_form(self):
        with app.test_client() as client:
            u = {"first_name": "TestUser2", "last_name": "TestUser2"}

            res = client.post("/users/new", data=u, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser2", html)
    
    def test_post_user_edit_form(self):
        with app.test_client() as client:
            u = User.query.get(self.user_id);
            u.first_name = 'Jack'
            u.last_name = 'Sparrow'
            
            res = client.post(f'/users/{self.user_id}/edit', follow_redirects = True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200);
            self.assertIn('<p>Success! Changed Jack Sparrow', html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html= res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('User Test User has been deleted', html)
    
# POST ROUTES FOR USER
########################################################################################
    def test_post_user_form(self):
        with app.test_client() as client:
            u = {"first_name": "TestUser2", "last_name": "TestUser2"}

            res = client.post("/users/new", data=u, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser2", html)
    
    def test_post_user_edit_form(self):
        with app.test_client() as client:
            u = User.query.get(self.user_id);
            u.first_name = 'Jack'
            u.last_name = 'Sparrow'
            
            res = client.post(f'/users/{self.user_id}/edit', follow_redirects = True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200);
            self.assertIn('<p>Success! Changed Jack Sparrow', html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html= res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('User Test User has been deleted', html)
    

#GET ROUTES FOR POST
########################################################################################

    def test_show_home_page(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('test', html)
            self.assertIn('Recent Blogly Posts', html)
                
    def test_show_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('By <a href="/users/', html)
    
    def test_show_post_form(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/posts/new') 
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('col-form-label">Title</label>', html)

    def test_show_edit_post_form(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit', html)

# POST ROUTES FOR POST
########################################################################################

    def test_post_post_form(self):
        with app.test_client() as client:
            p = {"title": "Test title2", "content": "Test content2", "user_id":f'{self.user_id}'}
            res = client.post(f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True)
            html = res.get_data(as_text=True)
        
            self.assertEqual(res.status_code, 200)
            self.assertIn("Test title2", html)    
    
    def test_post_edit_post_form(self):
        with app.test_client() as client:
            p = Post.query.get(self.post_id);
            p.title = 'Test2'
            res = client.post(f'/posts/{self.post_id}/edit', follow_redirects = True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Successfully changed &#34;Test2&#34;', html)
    
    def test_delete_post(self):
        with app.test_client() as client:
            res = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html= res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Post &#34;test&#34; has been deleted</p>', html)

#GET ROUTES FOR TAGS
########################################################################################

    def test_show_tag_list(self):
        with app.test_client() as client:
            res = client.get("/tags")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('tag', html)
                
    def test_show_tag(cls):
        with app.test_client() as client:
            res = client.get(f'/tags/{cls.tag_id}')
            html = res.get_data(as_text=True)
            cls.assertEqual(res.status_code, 200)
            cls.assertIn('<h1 class="ml-2">tag</h1>', html)
    
    def test_show_tag_form(cls):
        with app.test_client() as client:
            res = client.get('/tags/new') 
            html = res.get_data(as_text=True)
            cls.assertEqual(res.status_code, 200)
            cls.assertIn('<label for="name" class="col-md-2 col-form-label">Name</label>', html)

    def test_show_edit_form_tag(cls):
        with app.test_client() as client:
            res = client.get(f'/tags/{cls.tag_id}/edit')
            html = res.get_data(as_text=True)

            cls.assertEqual(res.status_code, 200)
            cls.assertIn('<input name="name" type="text" value="tag" />', html)
    

# POST ROUTES FOR TAGS
########################################################################################

    def test_post_tag_form(self):
        with app.test_client() as client:
            t = {"name": "tag2"}
            res = client.post(f"/tags/new", data=t, follow_redirects=True)
            html = res.get_data(as_text=True)
        
            self.assertEqual(res.status_code, 200)
            self.assertIn('href="/tags/2">tag2</a>', html)    
    
    def test_post_edit_tag_form(cls):
        with app.test_client() as client:
            t = Tag.query.get(cls.tag_id);
            t.name = 'tag2'
            res = client.post(f'/tags/{cls.tag_id}/edit', follow_redirects = True)
            html = res.get_data(as_text=True)

            cls.assertEqual(res.status_code, 200)
            cls.assertIn('<p>Updated tag &#34;tag2&#34;', html)
            
    def test_delete_tag(cls):
        with app.test_client() as client:
            res = client.post(f'/tags/{cls.tag_id}/delete', follow_redirects=True)
            html= res.get_data(as_text=True)

            cls.assertEqual(res.status_code, 200)
            cls.assertIn('<p>Tag &#34;tag&#34; has been deleted</p>', html)
