from app.main import main
from flask import render_template, request, send_from_directory, current_app
from app import db
from app.models import Post

@main.route("/")
def home():
    page_number = request.args.get('page_number', 1 , type=int)
    Posts = db.paginate(Post.query.order_by(Post.date_posted.desc()), page=page_number, per_page=5)
    return render_template("home.html", posts=Posts)

@main.route("/about")
def about():
    return render_template("about.html", title="About")

@main.route("/health")
def health_check():
    return "The backend is running"

@main.route("/serve/<filename>")
def serve_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)