#! /usr/bin/env python
# coding: utf-8

import unittest, sys
# sys.path.append('./src/app/scripts/')
from urllib import urlopen


class MyTestCase(unittest.TestCase):
	def test_user_registeration(self):
		delete_user('test@test.com')

		# Register
		page = urlopen('http://localhost/signup?email=test@test.com&password=testtest').read()
		# print page
		assert 'success' in page  # 'failure'

		# Is signed in
		page = urlopen('http://localhost/signedin').read()
		print page
		assert 'test@test.com' in page  # 'none' or the email

		# # sign in
		# page = urlopen('http://localhost/signin?email=test@test.com&password=testtest').read()
		# assert 'success' in page
		#
		# # sign out
		# page = urlopen('http://localhost/signout').read()
		# assert 'success' in page
		#
		# # Is signed in -> Not
		# page = urlopen('http://localhost/signedin').read()
		# assert 'none' in page # 'none' or the email

		delete_user('test@test.com')


def delete_user(email):
	import MySQLdb as mysql

	user = 'root'
	password = 'secret'
	server = 'localhost'
	db = 'NewFamilyCode'
	con = mysql.connect(server, user, password, db, charset='utf8', use_unicode=True)
	cur = con.cursor()
	cur.execute('delete from Zabayen where Email = %s', (email,))
	con.commit()
	con.close()


if __name__ == '__main__':
	unittest.main()
