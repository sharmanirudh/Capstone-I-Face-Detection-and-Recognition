from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, MultipleFileField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login', id='login_button')



class SignUpForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
							validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField('Confirm Password', 
						validators=[DataRequired(), Length(min=4, max=20), EqualTo('password', message='Confirm password must match Password.')])
	submit = SubmitField('Sign up', id='login_button')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists.')



class RegistrationForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Register')