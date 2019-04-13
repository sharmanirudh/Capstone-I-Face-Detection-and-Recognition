from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, MultipleFileField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	name = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField('Confirm Password', 
						validators=[DataRequired(), Length(min=4, max=20), EqualTo('password')])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	name = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField = ('Login')