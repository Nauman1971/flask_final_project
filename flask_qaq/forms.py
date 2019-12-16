from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf.file import FileField, FileRequired


class SignupForm(FlaskForm):
    username = StringField('Name', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    # password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=200)])
    number = IntegerField("Number")
    roles = SelectField("Roles", choices=[('Teacher', 'Teacher'), ('Student', 'Student')])
    # file = FileField(validators=[FileRequired()])


class LoginForm(FlaskForm):
    username = StringField("Name", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=200)])
