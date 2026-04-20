from flask import flash, jsonify, redirect, render_template, request, url_for
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

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
        user_found = User.query.filter(User.email == form.email.data).first()
        if(user_found):
            check_pw = bcrypt.check_password_hash(user_found.password, form.password.data)
            if(check_pw):
                flash(f"Logged in Successfully as {user_found.username}!", "success")
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password", "danger")
                return render_template("login.html", form=form, title="Login")
        else:
            flash("No Such User!", "danger")
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