"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

PostTag.query.delete()
Post.query.delete()
Tag.query.delete()
User.query.delete()

john = User(
    first_name='John',
    last_name='Smith',
)
kevin = User(
    first_name='Kevin',
    last_name='Moreth',
)
hannah = User(
    first_name='Hannah',
    last_name='Bark',
)
juliette = User(
    first_name='Juliette',
    last_name='Johnson',
)
fun = Tag(
    name='fun',
)
love = Tag(
    name='love',
)
travel = Tag(
    name='travel',
)
lol = Tag(
    name='lol',
)

db.session.add_all([john, kevin, hannah, juliette, fun, love, travel, lol])
db.session.commit()

post1 = Post(
    title='Hey y\'all!',
    content='I\'m going to Florida this weekend.',
    user_id=juliette.id
)
post2 = Post(
    title='Hello world!',
    content='My dog and I love to walk around the park.',
    user_id=hannah.id
)
post3 = Post(
    title='This is a joke',
    content='I\'m really bad at telling jokes.',
    user_id=kevin.id
)
post4 = Post(
    title='Hi!',
    content='I have nothing to say!',
    user_id=john.id
)

db.session.add_all([post1, post2, post3, post4])
db.session.commit()

post1_tag1 = PostTag(
    post_id=post1.id,
    tag_id=fun.id,
)
post1_tag2 = PostTag(
    post_id=post1.id,
    tag_id=travel.id,
)
post1_tag3 = PostTag(
    post_id=post1.id,
    tag_id=love.id,
)
post2_tag1 = PostTag(
    post_id=post2.id,
    tag_id=love.id,
)
post2_tag2 = PostTag(
    post_id=post2.id,
    tag_id=fun.id,
)
post3_tag1 = PostTag(
    post_id=post3.id,
    tag_id=lol.id,
)

db.session.add_all(
    [post1_tag1, post1_tag2, post1_tag3, post2_tag1, post2_tag2, post3_tag1]
)
db.session.commit()
