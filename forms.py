from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

max_of_20 = "Max length is 20 Characters"


class RegisterForm(FlaskForm):
    """User Registration Form"""
    first_name = StringField("First Name", validators=[
                             InputRequired("First name is required"), Length(max=20, message=max_of_20)])

    last_name = StringField("Last Name", validators=[
                            InputRequired("Last name is required"),
                            Length(max=20, message=max_of_20)])

    email = StringField("Email Address", validators=[InputRequired(
        "Email is required"), Email(message="Must be an email address"), Length(max=50, message="Max length is 50 Characters")])

    username = StringField("Username", validators=[
                           InputRequired("Username is required"), Length(max=20, message=max_of_20)])

    password = PasswordField("Password", validators=[
        InputRequired("Password is required")])


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("Username", validators=[
        InputRequired("Username is required"), Length(max=20, message="Max length is 20 Characters")])

    password = PasswordField("Password", validators=[
        InputRequired("Password is required")])


class FeedbackForm(FlaskForm):
    """Feedback Form"""
    title = StringField("Title", validators=[
                        InputRequired("Title is required"), Length(max=100, message="Max length is 100 characters")])

    content = TextAreaField("Content", validators=[
        InputRequired("Must add some content")])
