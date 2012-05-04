#!/usr/bin/env python
# coding: utf-8
from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email

class LoginForm(Form):
	login = TextField('Username or E-Mail', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])

class SignupForm(Form):
	email = TextField('E-Mail', validators=[Required(), Email()])
	username = TextField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
