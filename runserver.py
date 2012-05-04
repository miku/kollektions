#!/usr/bin/env python
# coding: utf-8

import argparse

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Kollektions')
	parser.add_argument('-s', '--server', metavar='SERVER', type=str,
		default='development', help='server setup, one of [development, gevent]')

	args = parser.parse_args()

	if args.server == 'development':
		from kollektions import app
		app.run(host='0.0.0.0', debug=True)

	elif args.server == 'gevent':
		from gevent.wsgi import WSGIServer
		from kollektions import app

		http_server = WSGIServer(('', 5000), app)
		http_server.serve_forever()
