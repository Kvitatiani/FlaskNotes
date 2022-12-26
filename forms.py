from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, URL, Length


class RegisterForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=7, max=32)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', validators=[DataRequired()])


class NotesForm(FlaskForm):
    text = CKEditorField('Add Note', validators=[DataRequired()])
    submit = SubmitField('Save Note')
