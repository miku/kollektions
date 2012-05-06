#!/usr/bin/env python
# coding: utf-8
from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, ValidationError
from kollektions.utils import calculate_sha1
from kollektions import db, User
from sqlalchemy import or_

class Length(object):
    """
    Verifies the length of the given input.
    """
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between %i and %i characters long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)

class LoginSuccessful(object):
    """
    Verifies user credentials through the 'user' table.
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        # user = get_user_by_username_or_email(form.data['login'])
        user = User.query.filter(or_(
            User.username==form.data['login'], 
            User.email==form.data['login'])).first()
        if user == None:
            raise ValidationError(self.message)
        # if not user.password == calculate_sha1(form.data['password']):
        if not user.password == form.data['password']:
            raise ValidationError(self.message)

class UniqueEmail(object):
    """
    Checks whether we already have this email.
    """
    def __init__(self, message):
        self.message = message
    def __call__(self, form, field):
        # user = get_user_by_email(field.data)
        user = User.query.filter(User.email==field.data).first()
        if not user == None:
            raise ValidationError(self.message)

class UniqueUsername(object):
    """
    Checks whether we already have this username.
    """
    def __init__(self, message):
        self.message = message
    def __call__(self, form, field):
        # user = get_user_by_username(field.data)
        user = User.query.filter(User.username==field.data).first()
        if not user == None:
            raise ValidationError(self.message)

class LoginForm(Form):
    """
    The actual login form.
    """
    login = TextField('Username or E-Mail', validators=[Required(), 
        LoginSuccessful(message='invalid username or password')])
    password = PasswordField('Password', validators=[Required()])


class SignupForm(Form):
    """
    Signup form.
    """
    email = TextField('E-Mail', validators=[Required(), Email(), 
        UniqueEmail(message='this email is taken, sorry'),
        Length(max=120)])
    username = TextField('Username', validators=[Required(), 
        UniqueUsername(message='this username is taken, sorry'),
        Length(max=80)])
    password = PasswordField('Password', validators=[Required(),
        # TODO change 1 to 6+
        Length(min=1, max=120)])
