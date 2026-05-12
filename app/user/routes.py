from app.user import user
from flask import render_template, redirect, flash, url_for, request, current_app
from app.user.forms import RegistrationForm, LoginForm, AccountForm, ResetPassword, ResetRequest
from app import db, bcrypt, mail
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from app.user.utils import check_url_scheme_and_authority, handle_pfp_uploads, create_jwt, verify_jwt
from pathlib import Path
from flask_mail import Message

@user.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("main.home"))
    return render_template("register.html", form=form, title="Sign Up")

@user.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("main.home"))
        else:
            flash("Incorrect Username or Password", "danger")
    return render_template("login.html", form=form, title="Login")

@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("main.home"))

@user.route("/account", methods=["GET", "POST"])
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

@user.route("/login/forgot_password", methods=["GET", "POST"])
def request_password_change():
    if current_user.is_authenticated:
        flash("Already Logged In", "info")
        return redirect(url_for("main.home"))
    form = ResetRequest()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        token = create_jwt(user.id)
        reset_url = url_for("user.create_new_password", token=token, _external=True)
        flash("An email has been sent to this email with further instructions", "info")
        msg = Message(subject="Request to reset your password",
                      html = render_template("password_reset_email.html", username = user.username, reset_url=reset_url),
                      body = f"""
                            Hello,
                            We have received a request to change your password.
                            Please follow this URL to change your password: {reset_url}
                            """ ,
                            recipients = [user.email]
                    )
        mail.send(msg)
    return render_template("reset_request.html", title="Forgot Password", form=form)

@user.route("/create_new_password/<token>", methods=["GET", "POST"])
def create_new_password(token):
    if current_user.is_authenticated:
        flash("Already Logged In", "info")
        return redirect(url_for("main.home"))
    data = verify_jwt(token)
    if not data:
        return redirect(url_for("user.request_password_change"))
    form = ResetPassword()
    if form.validate_on_submit():
        user = db.session.get(User, data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(encoding="utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Password changed successfully, please login to your account", "success")
        return redirect(url_for("user.login"))
    return render_template("reset_password.html", title="Create New Password", form=form)