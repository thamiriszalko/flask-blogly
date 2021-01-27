from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5433/blogly_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name="First", last_name="Last")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Last', html)

    def test_show_pet(self):
        with app.test_client() as client:
            resp = client.get(f'users/{self.user_id}/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h5>First Last</h5>', html)

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

    def test_edit_user_get(self):
        with app.test_client() as client:
            resp = client.get(
                f"/users/{self.user_id}/edit",
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("Last", html)

    def test_detail_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/detail")
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertIn("First", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(
                f"/users/{self.user_id}/delete",
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(200, resp.status_code)
            self.assertNotIn("First Last", html)
