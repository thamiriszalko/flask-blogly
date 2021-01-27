from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


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
