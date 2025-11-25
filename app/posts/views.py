from flask import render_template, request, redirect, url_for, flash, session
from . import posts_bp
from app import db
from .forms import PostForm, DeleteForm
from .models import Post, PostCategory, Tag
from app.users.models import User


@posts_bp.route('/create', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    users = db.session.scalars(db.select(User).order_by(User.username)).all()
    form.author_id.choices = [(user.id, user.username) for user in users]
    tags = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        selected_tags = []
        if form.tags.data:
            selected_tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,
            user_id=form.author_id.data,
            tags=selected_tags
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f"Post {new_post.title} has been created!", 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('add_post.html', form=form, title="Create Post",
                           action_url=url_for('posts.add_post'))


@posts_bp.route('/')
def get_posts():
    all_posts = db.session.execute(
        db.select(Post).order_by(Post.posted.desc())
    ).scalars().all()

    return render_template('all_posts.html', posts=all_posts, title="All Posts")


@posts_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post, title=post.title)


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    users = db.session.scalars(db.select(User).order_by(User.username)).all()
    form.author_id.choices = [(user.id, user.username) for user in users]
    tags = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = PostCategory(form.category.data)
        post.posted = form.publish_date.data
        post.is_active = form.is_active.data
        post.user_id = form.author_id.data

        if form.tags.data:
            selected_tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            post.tags = selected_tags
        else:
            post.tags = []

        db.session.commit()

        flash(f"Post {post.title} has been updated!", 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template('add_post.html', form=form, title="Edit Post",
                           action_url=url_for('posts.edit_post', id=post.id),
                           post=post)


@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    form = DeleteForm()

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash(f"Post {post.title} has been deleted.", 'danger')
        return redirect(url_for('posts.get_posts'))

    return render_template('delete_confirm.html', post=post, form=form, title="Confirm Deletion")