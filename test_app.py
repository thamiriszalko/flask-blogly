from unittest import TestCase

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5433/blogly_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(
            first_name="First",
            last_name="Last"
        )
        db.session.add(user)
        db.session.commit()
        post = Post(
            title='This is the title',
            content='This is the content',
            user_id=user.id
        )
        db.session.add(post)
        tag = Tag(
            name='tag12',
        )
        db.session.add(tag)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.tag_id = tag.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Last', html)

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/detail")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('This is the title', html)

    def test_detail_user(self):
        with app.test_client() as client:
            resp = client.get(f'users/{self.user_id}/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h5>First Last</h5>', html)

    def test_detail_post(self):
        with app.test_client() as client:
            resp = client.get(f'posts/{self.post_id}/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('By First Last', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post(
                "/users/new",
                data=dict(
                    first_name='First',
                    last_name='Last',
                    profile_img=None,
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("First Last", html)

    def test_add_post(self):
        with app.test_client() as client:
            resp = client.post(
                f"/posts/{self.user_id}/new",
                data=dict(
                    title='Title',
                    content='Content',
                    user_id=self.user_id
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("Title", html)

    def test_edit_user_post(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/edit",
                data=dict(
                    first_name='Last',
                    last_name='First',
                    profile_img=None,
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("Last First", html)

    def test_edit_post_post(self):
        with app.test_client() as client:
            resp = client.post(
                f"/posts/{self.post_id}/edit",
                data=dict(
                    title='This is one title',
                    content='Content for everyone',
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("This is one title", html)

    def test_edit_user_get(self):
        with app.test_client() as client:
            resp = client.get(
                f"/users/{self.user_id}/edit",
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("Last", html)

    def test_edit_post_get(self):
        with app.test_client() as client:
            resp = client.get(
                f"/posts/{self.post_id}/edit",
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("This is the content", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(
                f"/users/{self.user_id}/delete",
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertNotIn("First Last", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.get(
                f"/posts/{self.post_id}/delete",
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertNotIn("This is the title", html)

    def test_add_tag(self):
        with app.test_client() as client:
            resp = client.post(
                "/tags/new",
                data=dict(
                    name='tag1',
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("tag1", html)

    def test_edit_tag_get(self):
        with app.test_client() as client:
            resp = client.get(
                f"/tags/{self.tag_id}/edit",
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("tag12", html)

    def test_edit_tag_post(self):
        with app.test_client() as client:
            resp = client.post(
                f"/tags/{self.tag_id}/edit",
                data=dict(
                    name='tag123',
                ),
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("tag123", html)