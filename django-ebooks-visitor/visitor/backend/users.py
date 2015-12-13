# coding: utf-8

from . import db
from django.http import HttpResponse

# database_names = ('NewFamilyCode', 'tabaraktafseerbookdb', 'arabiclaws')
# mysql_port = 3306


def sign_in(mail, password):
	output = get_user(mail, password)
	response = HttpResponse(output)
	if output == 'success':
		response.set_cookie("family_loggedIn", "true")
		response.set_cookie("family_email", mail)
	else:
		response.set_cookie("family_loggedIn", "false")
		response.set_cookie("family_email", "")

	return response


def get_user(email, password):
	import hashlib
	import re
	if len(email) < 7 or re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
		return "Invalid email format"
	elif len(password) < 7:
		return "Too short password"
	con, cur = db.get_con()
	cur.execute('SELECT Email, Pass, Salt FROM visitor_zabayen WHERE Email = %s', (email, ))

	userInfo = cur.fetchone()

	if userInfo == None:
		con.close()
		return "user email does not exist"
	elif hashlib.sha1(password + userInfo[2]).hexdigest() != userInfo[1]:
		con.close()
		return "Invalid password"
	else:
		con.close()
		return "success"


def add_user(email, password, password2):
	import hashlib
	import random
	import re
	import json
	import time

	if len(email) < 7 or re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
		return ">Email is not accepted:", email
	elif len(password) < 7:
		return ">Password is not accepted:", password

	salt = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(40))
	hashed_pass = hashlib.sha1(password + salt).hexdigest()

	con, cur = db.get_con()
	cur.execute('SELECT Email FROM visitor_zabayen WHERE Email = %s', (email, ))

	userInfo = cur.fetchone()

	if userInfo == None:
		# try:
		cur.execute('INSERT INTO visitor_zabayen (Email, Pass, Salt) VALUES(%s, %s, %s)', (email, hashed_pass, salt))
		con.commit()
		con.close()
		return "success"
		# except:
		# 	import sys
		# 	print "Unexpected error:", sys.exc_info()[0]
		# 	raise
			# con.rollback()
			# con.close()
			#
			# return "Exception happened!!"

	else:
		con.close()
		return "email exist!"


def del_user(email):
	con, cur = db.get_con()
	query = 'DELETE FROM visitor_zabayen WHERE Email = %s'
	try:
		cur.execute(query, (email,))
		con.commit()
		return True
	except:
		con.rollback()
		return False


def get_logged_email(request):
	key = "family_email"
	value = request.COOKIES[key]
	if not value:
		value = ""

	return value


def is_logged_in(request):
	key = "family_loggedIn"

	try:
		logged = request.COOKIES[key]
	except:
		return False

	logged = request.COOKIES[key]
	return logged == "true"
