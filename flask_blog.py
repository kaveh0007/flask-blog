from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = (
    "cbd535a731c27deae6fc9e9c2fbb12225cb321c530fddcf272c6a606b24dca58"
)

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
    if form.validate_on_submit():
        if form.email.data == "kaveh@blog.com" and form.password.data == "password":
            flash("Logged in Successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials!", "danger")
    return render_template("login.html", form=form, title="Login")