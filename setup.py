#!/usr/bin/env python

from distutils.core import setup
try:
	import setuptools # enable: python setup.py develop
except ImportError, ie:
	pass

setup(
	name='kollektions',
	version='0.0.1',
	description='Your library network.',
	# url='http://NA',
	author='Martin Czygan',
	author_email='martin.czygan@gmail.com',
	packages=[
		'kollektions',
	],
	package_data={
	},
	scripts=[
	],
	classifiers=[
		# TODO
	],
)
