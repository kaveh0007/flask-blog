from app import app
from flask import render_template, url_for, flash, redirect, request, jsonify
from app.forms import RegistrationForm, LoginForm

Posts = [
    {
        "author": "Kaveh",
        "title": "Blog Post 1",
        "date_posted": "October 24, 2025",
        "content": "Hello this is my first blog post",
    },
    {
        "author": "John Doe",
        "title": "Blog Post 1",
        "date_posted": "October 24, 2025",
        "content": "Hello now the AWS server in east US just went down",
    },
]

@app.route("/")
def home():
    return render_template("home.html", posts=Posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/health")
def health_check():
    return "The backend is running"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form, title="Sign Up")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if request.method=="POST" && form.validate()
        if form.email.data == "kaveh@blog.com" and form.password.data == "password":
            flash("Logged in Successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials!", "danger")
    return render_template("login.html", form=form, title="Login")

@app.route("/posts/by/<author>")
def posts_by_author(author):
    author_posts=[]
    for post in Posts:
        if post["author"] == author:
            author_posts.append(post)
    if author_posts:
        return render_template("home.html", posts=author_posts, author=author)
    return render_template("author_not_found.html", author=author)

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    author=data['author']
    redirect_url=url_for('posts_by_author', author=author)
    return jsonify({"redirect_url": redirect_url})