from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,BooleanField
from wtforms.validators import DataRequired,Regexp,Length,Email
from ..models import Role,User
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('What is your name?',validators=[Regexp('\w+')]) #wei kong
    submit = SubmitField('Submit',validators=[DataRequired()])


class EditProfileForm(Form):
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username',validators=[DataRequired(),Length(1,64),
                                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                         'Usernames must have only letters,'
                                                         'numbers,dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Role name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    body = PageDownField("What's on your mind? (support Markdown)",validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('',validators=[DataRequired()])
    submit = SubmitField('Submit')
