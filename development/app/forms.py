from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, MultipleFileField, PasswordField, SubmitField, BooleanField, HiddenField
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


class DetectionForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	submit = SubmitField('Detect')


class RegistrationForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
	submit = SubmitField('Register')


class RecognizeForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	submit = SubmitField('Recognize')


class UpdateAccountForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
							validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField('Confirm Password', 
						validators=[DataRequired(), Length(min=4, max=20), EqualTo('password', message='Confirm password must match Password.')])
	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already exists.')

class UpdateDatasetForm(FlaskForm):
	images = MultipleFileField('User Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('New name', validators=[DataRequired(), Length(min=2, max=40)])
	images_to_be_deleted = HiddenField('Images to be deleted', validators=[])
	submit = SubmitField('Update') 