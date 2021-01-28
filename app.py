"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5433/blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123-456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def landing_page():
    users = User.query.all()

    return render_template("landing_page.html", users=users)


@app.route('/users/new', methods=["GET", "POST"])
def user_form():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_img = request.form.get('profile_img')

        user = User(
            first_name=first_name,
            last_name=last_name,
            img_url=profile_img
        )
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:

        return render_template("user_form.html")


@app.route('/users/<int:user_id>/detail')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template("user_detail.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit', methods=["POST", "GET"])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.img_url = request.form.get('profile_img')
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('user_edit.html', user=user)


@app.route('/users/<int:user_id>/delete')
def user_delete(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/')


@app.route('/posts/<int:post_id>/detail')
def post_detail(post_id):
    print('post_id', post_id)
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("post_detail.html", user=user, post=post)


@app.route('/posts/<int:user_id>/new', methods=["GET", "POST"])
def post_form(user_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = user_id

        post = Post(
            title=title,
            content=content,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user_id}/detail')
    else:

        return render_template("post_form.html", user_id=user_id)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{post.user_id}/detail')
    else:

        return render_template("post_edit.html", post=post)


@app.route('/posts/<int:post_id>/delete')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{post.user_id}/detail')
