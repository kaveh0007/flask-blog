from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, EqualTo
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords do not match!"),
        ],
    )
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if(user):
            raise ValidationError('That username is taken, please choose a different one')
        
    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if(user):
            raise ValidationError('An account already exists with this email')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password")
    remember = BooleanField()
    submit = SubmitField("Login")

class AccountForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    image_file = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter(User.username == username.data).first()
            if(user):
                raise ValidationError('That username is taken, please choose a different one')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter(User.email == email.data).first()
            if(user):
                raise ValidationError('An account already exists with this email')