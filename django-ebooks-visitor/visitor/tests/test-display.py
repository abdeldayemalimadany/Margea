#! /usr/bin/env python
# coding: utf-8

# import unittest
from backend import page
from django.test import TestCase

# from family.display.backend import page
# import pydevd
#
# #sudo pip install pydevd
# pydevd.settrace('localhost', port=9980)

class TestSearch_book0(TestCase):
	"""Test scenarios for search"""
	# These vars are shared between all instances. something like static

	def setUp(self):
		self.db_index = 0

	def test_display_book_0(self):
		page_only = True
		page_serial = '1'
		my_page = page.get_page(page_serial)
		self.assertIn('{"path": ', my_page)
		print my_page

# class TestSearch_book1(TestSearch_book0, unittest.TestCase):
# 	def setUp(self):
# 		self.db_index = 1
#
#
# class TestSearch_book2(TestSearch_book0, unittest.TestCase):
# 	def setUp(self):
# 		self.db_index = 2


# if __name__ == '__main__':
# 	unittest.main()
#
