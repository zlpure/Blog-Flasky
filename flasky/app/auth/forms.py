from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username',validators=[
        DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                           'Username must have only letters(first),'
                                           'numbers,dot or underscores')])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',
                                                                           message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_eamil(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class ChangePassword(Form):
    old_password = PasswordField('Old Password',validators=[DataRequired()])
    password = PasswordField('New Password',validators=[DataRequired()])
    password2 = PasswordField('Confirm new password',validators=[DataRequired(),EqualTo('password',message='Passwords must match')])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')