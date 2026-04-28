from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.utils import check_url_scheme_and_authority

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
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form, title="Sign Up")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if request.method=="POST" && form.validate()
        user = User.query.filter(User.email == form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Logged in Successfully as {user.username}", "success")
            # In case a login_required functionality was accessed by an unauthenticated user
            next = request.args.get('next')
            if check_url_scheme_and_authority(next, request.host):
                return redirect(next)
            else:
                flash("Unverified URLs cannot be accessed", "danger")
                return redirect(url_for("home"))
        else:
            flash("Incorrect Username or Password", "danger")
    return render_template("login.html", form=form, title="Login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

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