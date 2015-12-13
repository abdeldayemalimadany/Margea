#! /usr/bin/env python
# coding: utf-8

from unittest import TestCase
import unittest
# import sys
# sys.path.append('./src/backend/')
from visitor.backend import search
# from visitor.backend import page
import json
# from django.test import TestCase

index_path = '../index/'


class TestSearchBook(TestCase):
	def test_hello_world(self):
		self.assertEqual(1, 1)

	def test_search_and(self):
		search_words = u'حقيقة العيوب في النكاح وأثرها في فسخ النكاح'
		page_number = 1
		option = "and"
		index_path = '../index/'
		result_string = search.search_mobile(search_words, page_number, option, index_path)
		result_obj = json.loads(result_string)
		# print 'total hits=', len(result_obj['result'])
		# print result_obj
		self.assertEqual(1, len(result_obj['result']))

	def test_search_or(self):
		search_words = u'حقيقة العيوب في النكاح وأثرها في فسخ النكاح'
		page_number = 1
		option = "or"
		result_string = search.search_mobile(search_words, page_number, option, index_path)
		result_obj = json.loads(result_string)
		# print 'total hits=', len(result_obj['result'])
		# print result_obj
		self.assertEqual(3651, int(result_obj['count']))

	def test_search_mobile(self):
		search_words = u'نكح'
		page_number = 1
		option = "or"
		result_string = search.search_mobile(search_words, page_number, option, index_path)
		result_obj = json.loads(result_string)
		# print result_obj
		self.assertEqual(18, result_obj['count'])
		self.assertEqual(10, len(result_obj['result']))
		page_number = 2
		result_string2 = search.search_mobile(search_words, page_number, option, index_path)
		# print "\n\n", result_string2
		result_obj = json.loads(result_string2)
		self.assertEqual(18, result_obj['count'])
		self.assertEqual(8, len(result_obj['result']))

	def test_get_words(self):
		self.assertEqual('w1 w2 w3...', search.shorten('w1 w2 w3 w4 w5', 3))
		self.assertEqual('w1 w2', search.shorten('w1 w2', 4))  # no shortning done
		self.assertEqual('w1 w2 w3...', search.shorten('  w1 w2    w3 w4 w5   ', 3))
		self.assertEqual('w1 w2', search.shorten('  w1    w2   ', 4))

	def test_suffix_query(self):
		words = search.suffix_query("w1 w2 w3")
		self.assertEqual(" *w1* *w2* *w3*", words)

	def test_search_prefix_or(self):
		search_words = u'سجد'
		option = 'or-fix'
		page_number = 1
		result_string = search.search_mobile(search_words, page_number, option, index_path)
		result_obj = json.loads(result_string)
		# print result_obj
		self.assertEqual(111, result_obj['count'])

	def test_search_prefix_and(self):
		search_words = u'سجد'
		option = 'and-fix'
		page_number = 1
		result_string = search.search_mobile(search_words, page_number, option, index_path)
		result_obj = json.loads(result_string)
		# print result_obj
		self.assertEqual(111, result_obj['count'])

	#
	# def test_search_prefix_many(self):
	# 	self.search_words = u'التفاخر  '
	# 	self.using_exact = '0'
	# 	result_string = search.getSearch(self.search_words, self.and_words, self.using_exact, self.using_root, self.exclude_words, self.ids, self.scope_pages, self.db_index, index_path=self.path)
	# 	result_obj = json.loads(result_string)
	# 	# print 'total hits=', len(result_obj['result'])
	# 	self.assertEqual(2, len(result_obj['result']))
	#
	#

#
# class TestSearchBook1(TestSearchBook0, TestCase):
# 	def setUp(self):
# 		self.db_index = 1
#
# class TestSearchBook2(TestSearchBook0, TestCase):
# 	def setUp(self):
# 		self.db_index = 2



if __name__ == '__main__':
	unittest.main()
