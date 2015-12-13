#! /usr/bin/env python
# coding: utf-8

import unittest
import sys
# sys.path.append('./src/backend/')
import json
# import src.backend.topics
from display.backend import topics
from display.backend import fehres


class TestTree_book0(unittest.TestCase):

	def setUp(self):
		self.db_index = 0

	def test_tree(self):
		topic = 1
		result_string = topics.browse_tree(self.db_index, topic)
		# print result_string
		result_obj = json.loads(result_string)
		self.assertEqual(2, len(result_obj))
		self.assertLessEqual(1, len(result_obj['head']))
		self.assertLess(5, len(result_obj['body']))

	def test_tree_serial(self):
		serial = 1
		result_string = topics.browse_tree_by_serial(self.db_index, serial)
		result_obj = json.loads(result_string)
		# print ">", result_string
		self.assertEqual(0, len(result_obj['body']))
		self.assertLess(1, len(result_obj['head']))

	def test_tree_topic_2(self):
		topic = 1
		result_string = topics.browse_tree(self.db_index, topic)
		# print result_string
		result_obj = json.loads(result_string)
		self.assertEqual(2, len(result_obj))
		self.assertLess(5, len(result_obj['body']))
		self.assertLessEqual(1, len(result_obj['head']))
		# print result_obj['head']


	def test_get_fehres(self):
		fehres_id = 0
		result_string = fehres.getFehres(self.db_index, fehres_id)
		result_obj = json.loads(result_string)
		self.assertLess(600, len(result_obj))


class TestTree_book1(TestTree_book0, unittest.TestCase):
	def setUp(self):
		self.db_index = 1


class TestTree_book2(TestTree_book0, unittest.TestCase):
	def setUp(self):
		self.db_index = 2


if __name__ == '__main__':
	unittest.main()

