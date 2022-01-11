from flask import (Blueprint, render_template, request, 
					redirect, abort, flash, url_for)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.form import PostForm

posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods = ["POST", "GET"])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("You have created a post", "success")
		return redirect(url_for("main.index"))
	return render_template("new_post.html",form = form, legend = 'new_post')

@posts.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template("post.html",posts = post)

@posts.route("/post/<int:post_id>/update", methods = ["POST", "GET"])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Post updated", 'success')
		return redirect(url_for("main.index"))
	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content
	return render_template("new_post.html",form = form, legend = 'update_post')

@posts.route("/post/<int:post_id>/delete", methods = ["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Post deleted", "success")
	return redirect(url_for("main.index"))