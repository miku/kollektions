#!/usr/bin/env python
# coding: utf-8
from flaskext.wtf import Form, TextField, PasswordField, Required

class LoginForm(Form):
	login = TextField('Username or E-Mail', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
