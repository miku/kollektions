#!/usr/bin/env python
# coding: utf-8
from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, ValidationError
import pyes
from kollektions.store import get_user, get_user_by_email, get_user_by_username
from kollektions.utils import calculate_sha1

class LoginSuccessful(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = get_user(form.data['login'])
        if user == None:
            raise ValidationError(self.message)
        if not user['password'] == calculate_sha1(form.data['password']):
            raise ValidationError(self.message)

class UniqueEmail(object):
    def __init__(self, message):
        self.message = message
    def __call__(self, form, field):
        user = get_user_by_email(field.data)
        if not user == None:
            raise ValidationError(self.message)

class UniqueUsername(object):
    def __init__(self, message):
        self.message = message
    def __call__(self, form, field):
        user = get_user_by_username(field.data)
        if not user == None:
            raise ValidationError(self.message)

class LoginForm(Form):
    login = TextField('Username or E-Mail', validators=[Required(), 
        LoginSuccessful(message='invalid username or password')])
    password = PasswordField('Password', validators=[Required()])


class SignupForm(Form):
    email = TextField('E-Mail', validators=[Required(), Email(), 
        UniqueEmail(message='this email is taken, sorry')])
    username = TextField('Username', validators=[Required(), 
        UniqueUsername(message='this username is taken, sorry')])
    password = PasswordField('Password', validators=[Required()])
