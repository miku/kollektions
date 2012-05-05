#!/usr/bin/env python
# coding: utf-8
from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, ValidationError
import pyes
import hashlib
from kollektions.store import get_user

def calculate_sha1(s):
    sha1 = hashlib.sha1()
    sha1.update(s)
    return sha1.hexdigest()

class LoginSuccessful(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = get_user(form.data['login'])
        if user == None:
            raise ValidationError('invalid username or password')
        if not calculate_sha1(user['password']) == form.data['password']:
            raise ValidationError('invalid username or password')

class LoginForm(Form):
    login = TextField('Username or E-Mail', validators=[Required(), LoginSuccessful()])
    password = PasswordField('Password', validators=[Required()])


class SignupForm(Form):
    email = TextField('E-Mail', validators=[Required(), Email()])
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
