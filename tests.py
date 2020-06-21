from datetime import datetime, timedelta
import unittest
from app import app
from app.database import db
from app.models import User, Post


class UserModelTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="Username", email="username@mail.ru")
        u.set_password("boom")
        self.assertFalse(u.check_password("moob"))
        self.assertTrue(u.check_password("boom"))

    def test_avatar(self):
        u = User(username="Username", email="username@mail.ru")
        self.assertEqual(u.get_avatar(123), "https://www.gravatar.com/avatar/d4a5a4a5f6baec652148c1ad992162b4?d=identicon&s=123")

    def test_create_users_and_follow(self):
        u1 = User(username="Username1", email="username1@mail.ru")
        u2 = User(username="Username2", email="username2@mail.ru")
        self.assertEqual(User.query.count(), 0)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(User.query.count(), 2)
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "Username2")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "Username1")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_followed_posts(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(
            body="post from john",
            author=u1,
            timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body="post from susan",
            author=u2,
            timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(
            body="post from mary",
            author=u3,
            timestamp=now + timedelta(seconds=3)
        )
        p4 = Post(
            body="post from david",
            author=u4,
            timestamp=now + timedelta(seconds=2)
        )
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    app_ctx = app.app_context()
    app_ctx.push()
    unittest.main(verbosity=2)
    app_ctx.pop()
