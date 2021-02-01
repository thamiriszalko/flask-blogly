"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5433/blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123-456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def landing_page():
    users = User.query.all()
    tags = Tag.query.all()

    return render_template("landing_page.html", users=users, tags=tags)


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
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template(
        "post_detail.html",
        user=user,
        post=post,
        tags=post.tags
    )


@app.route('/posts/<int:user_id>/new', methods=["GET", "POST"])
def post_form(user_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags_ids = request.form.getlist('tag')
        post = Post(
            title=title,
            content=content,
            user_id=user_id
        )

        db.session.add(post)

        for tag_id in tags_ids:
            post.tags.append(
                Tag.query.get_or_404(tag_id)
            )

        db.session.commit()

        return redirect(f'/users/{user_id}/detail')
    else:
        tags = Tag.query.all()

        return render_template("post_form.html", user_id=user_id, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        tags_ids = request.form.getlist('tag')
        PostTag.query.filter_by(post_id=post.id).delete()
        for tag_id in tags_ids:
            post.tags.append(
                Tag.query.get_or_404(tag_id)
            )

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{post.user_id}/detail')
    else:
        tags = Tag.query.all()

        return render_template("post_edit.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{post.user_id}/detail')


@app.route('/tags/new', methods=["GET", "POST"])
def tag_form():
    if request.method == 'POST':
        name = request.form['name']

        tag = Tag(
            name=name,
        )
        db.session.add(tag)
        db.session.commit()

        return redirect('/')
    else:

        return render_template("tag_form.html")


@app.route('/tags/<int:tag_id>/detail')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_detail.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST", "GET"])
def tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.add(tag)
        db.session.commit()

        return redirect(f'/tags/{tag.id}/detail')
    else:
        return render_template('tag_edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete')
def tag_delete(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/')
