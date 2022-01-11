from flask import Blueprint,render_template, request
from flaskblog.models import Post


main = Blueprint('main',__name__)

@main.route("/")
@main.route("/index")
def index():
	page = request.args.get('page', 1, type = int)
	post = Post.query.order_by(Post.date.desc()).paginate(per_page=5,page = page)
	return render_template("index.html",posts = post)

@main.route("/about")
def about():
	return render_template("about.html", title = "its' about you")
