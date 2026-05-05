from flask import current_app, flash, jsonify, redirect, render_template, request, send_from_directory, url_for, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm, AccountForm, PostForm
from app.models import User, Post
from app.utils import check_url_scheme_and_authority, handle_pfp_uploads
from pathlib import Path

@app.route("/")
def home():
    Posts = Post.query.all()
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
            if(next):
                if check_url_scheme_and_authority(next, {request.host}):
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

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if(form.image_file.data):
            image_file = handle_pfp_uploads(form.image_file.data)
            previous_image_file = current_user.image_file
            if previous_image_file != "default.jpg":
                Path.unlink(f"{current_app.config['UPLOAD_FOLDER']}/{previous_image_file}")
            current_user.image_file = image_file
        db.session.commit()
        flash("Account updated successfully!", "success")

    filename = None
    if current_user.image_file != 'default.jpg':
        filename = current_user.image_file

    return render_template("account.html", form=form, title="Account", filename=filename)

@app.route("/serve/<filename>")
def serve_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    legend = "What's on your mind?"
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You successfully made a post", "success")
        return redirect(url_for('home'))
    return render_template("create_post.html", title="Create New Post", form=form, legend=legend)

@app.route("/post/<int:post_id>")
@login_required
def view_post(post_id):
    post=db.session.get(Post, post_id)
    return render_template("post.html", post=post, title=f"Post {post.id} by {current_user}")

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = db.session.get(Post, post_id)
    legend = "Update Post"

    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("home"))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template("create_post.html", title=f"Update Post {post_id}", form=form, legend = legend)

@app.route("/posts/by/<author>")
def posts_by_author(author):
    author_posts=[]
    for post in Post.query.all():
        if post.author.username == author:
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