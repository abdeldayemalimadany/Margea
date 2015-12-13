#! /usr/bin/env python
# coding: utf-8

import unittest
from urllib import urlopen

#http://188.166.21.10
#http://188.166.21.10/app/scripts/page.py?pageOnly=1&pageSerial=1
#http://188.166.21.10/app/scripts/search.py?_dc=1424365364441&word=%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87&all=1&exact=1&root=0&exclude=&ids=all&pages=all
#http://188.166.21.10/app/scripts/search.py?_dc=1424365364441&word=%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87&all=1&exact=1&root=0&exclude=&ids=all&pages=all

flag = 'digitalOcean'
# flag = 'vagrant'
# flag = 'macpro'


def decompress(data):
	import cStringIO, gzip

	s = cStringIO.StringIO()
	with gzip.GzipFile(fileobj=s, mode='rb') as f:
		f.read(data)

	return s.getvalue()


class TestSearch(unittest.TestCase):

	def setUp(self):
		if flag == 'digitalOcean':
			self.server = 'http://188.166.21.10'
		elif flag == 'macpro':
			self.server = 'http://localhost:9980'
		elif flag == 'vagrant':
			self.server = 'http://localhost'

	# def test_home_page(self):
	# 	text = urlopen(self.server).read()
	# 	# self.assertEquals(3121, len(text))
	# 	assert 'مدونة الأسرة السعودية' in text
	# 	# self.assertTrue( 'مدونة الأسرة السعودية' in text)
	#
	#
	# def test_display(self):
	# 	page = urlopen(self.server + '/app/scripts/page.py?pageOnly=1&pageSerial=1').read()
	# 	# self.assertEqual(3339, len(page))
	# 	assert 'الموافقة عليها من قبل المرأة' in page
	#
	# def test_search(self):
	# 	page = urlopen(self.server + '/app/scripts/search.py?_dc=1424365364441&word=%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87&all=1&exact=1&root=0&exclude=&ids=all&pages=all').read()
	# 	assert len(page) > 300

	def test_tree(self):
		import json

		page_json = urlopen('http://localhost/app/scripts/topics.py?topic=1').read()
		page_obj = json.loads(page_json)

		self.assertEquals(1, len(page_obj['head']))
		self.assertEquals(6, len(page_obj['body']))


	def test_tree_serial(self):
		import json

		page_json = urlopen('http://localhost/app/scripts/topics.py?serial=1').read()
		page_obj = json.loads(page_json)

		self.assertEquals(5, len(page_obj['head']))
		self.assertEquals(0, len(page_obj['body']))



	# def test_search_mobile(self):
	# 	# service = self.server + "/app/scripts/search.py?word=%D9%82%D8%A7%D9%84&mobile=y&page=1"
	# 	service = "http://localhost/app/scripts/search.py?word=%D9%86%D9%83%D8%AD&all=1&exact=1&root=0&exclude=&ids=all&pages=all&mobile=n&page=1"
	# 	page = urlopen(service).read()
	#
	# 	print("> decompress: " + decompress(page))
	# 	# assert len(page) > 300

if __name__ == '__main__':
	unittest.main()






