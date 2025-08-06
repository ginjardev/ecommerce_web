from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FloatField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired,length, NumberRange


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Log in')