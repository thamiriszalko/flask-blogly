from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    title = db.Column(
        db.Text,
        nullable=False,
    )
    content = db.Column(
        db.Text,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )
    tags = db.relationship(
        'Tag', secondary="post_tag", backref="posts")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    first_name = db.Column(
        db.Text,
        nullable=False,
    )
    last_name = db.Column(
        db.Text,
        nullable=False,
    )
    img_url = db.Column(
        db.Text,
        nullable=True,
        default='https://t4.ftcdn.net/jpg/03/46/93/61/360_F_346936114_RaxE6OQogebgAWTalE1myseY1Hbb5qPM.jpg',  # noqa
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.Text,
        nullable=False,
    )


class PostTag(db.Model):
    __tablename__ = "post_tag"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True
    )
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )


