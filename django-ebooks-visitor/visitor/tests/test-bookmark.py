#! /usr/bin/env python
# coding: utf-8

import unittest

# See relative imports: https://docs.python.org/2.5/whatsnew/pep-328.html

from backend import db
from visitor.backend import bookmark


class TestBookmarks(unittest.TestCase):
	"""Test scenarios for search"""
	# These vars are shared between all instances. something like static

	def setUp(self):
		self.db_index = 0
		self.email = 'test@test.com'

	def test_save(self):
		page_only = True
		page_serial = '1'
		# db.mysql_port = 9906
		import uuid
		record_id = uuid.uuid1()
		my_page = bookmark.set_bookmark(self.db_index, record_id, self.email, page_serial, 'some title', '')
		bookmark.del_bookmark(self.db_index, record_id)
		# I assume it is difficult for save and delete both to fail at the same time


	def test_get_list(self):
		result_string = bookmark.get_bookmarks(self.db_index, self.email)
		self.assertEquals('[]', result_string) #  it must be empty

	def test_register(self):
		password = "some password"
		added = db.add_user(self.db_index, self.email, password)
		self.assertTrue(added, 'Unable to add!!')

		exist = db.get_user(self.db_index, self.email, password)
		self.assertTrue(exist)

		deleted = db.del_user(self.db_index, self.email)
		self.assertTrue(deleted, 'Unable to remove!!')


if __name__ == '__main__':
	unittest.main()

