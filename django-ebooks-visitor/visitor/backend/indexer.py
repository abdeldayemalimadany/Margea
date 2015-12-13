#! /usr/bin/env python
# coding: utf-8

from whoosh.index import create_in
from whoosh.fields import *
import os


# TODO: Research Arabic light stemer: http://tashaphyne.sourceforge.net
# TODO: strip html tags: depends on using your own highlighting algo
# TODO: strip stop words
def print_progress(count):
	if count % 40 == 0:
		print '.',
		sys.stdout.flush()
	if count % 1100 == 0:
		print('\n')
		sys.stdout.flush()


def index_docs(django_db):
	print("This tool indexes database based on Whoosh full text engine.")
	index_text(django_db)
	index_toc(django_db)


def index_text(django_db):
	print("Indexing full article text")
	schema = Schema(page=TEXT(stored=False), serial=TEXT(stored=True), title=TEXT(stored=True),
	                parent_title=TEXT(stored=True))
	index_folder = "index/"
	if not os.path.exists(index_folder):
		print "Create folder", index_folder
		os.makedirs(index_folder)

	ix = create_in(index_folder, schema, indexname="text-index")
	writer = ix.writer()
	con, cur = get_con_by_db(django_db)
	query = 'SELECT PageText, SerialPageID, PageID, TopicID, TopicName FROM Topics_Data'
	cur.execute(query)

	record_set = cur.fetchall()
	count = 0
	if record_set is not None:
		for record in record_set:
			# try:
			count += 1
			page_text = record[0]
			page_serial = record[1]
			page_id = record[2]
			topic_id = record[3]
			page_title = record[4]
			footnote = get_footnotes(cur, topic_id, page_id)
			if page_text is None:
				page_text = u'NULL'
			if footnote is None:
				footnote = u'NULL'
			full_text = page_text
			if footnote and footnote is not None:
				full_text += footnote
			full_text = _strip_diacritics(full_text)
			parent_title = get_parent_title_by_topic_id(con, cur, topic_id)
			parent_title = _strip_diacritics(parent_title)
			if len(parent_title) < 1:
				writer.add_document(page=full_text, serial=str(page_serial).decode('utf-8'), title=page_title)
			else:
				writer.add_document(page=full_text, serial=str(page_serial).decode('utf-8'), title=page_title,
				                    parent_title=parent_title)

			print_progress(count)
			# except:
			# 	e = sys.exc_info()
			# 	print "Error:, ", e
			# 	print "index: ", count - 1
			# 	print "page_serial: ", page_serial
			# 	print "page_title: ", page_title.encode('utf-8')
			# 	print "full_text: ", full_text.encode('utf-8')
			# 	con.ping(True)
			# 	exit(-1)

	con.close()
	writer.commit()
	print '\n', count, 'records are indexed successfully.'


def get_footnotes(cur, topic_id, page_id):
	query = 'SELECT FootNoteID, FootNoteText FROM TopicsFootNotes WHERE TopicID = %s AND PageID = %s ORDER BY FootNoteID'
	cur.execute(query, (topic_id, page_id))
	result = cur.fetchall()
	footnote = ''
	if result is not None:
		for row in result:
			footnote += ' (%d) %s ' % (row[0], row[1])
	return _strip_diacritics(footnote)


def _strip_diacritics(text):
	import unicodedata
	# return ''.join([c for c in unicodedata.normalize('NFD', text) \
	# if unicodedata.category(c) != 'Mn'])
	if text and len(text) > 0:
		return ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
	else:
		return ''


def get_con_by_db(django_db):
	import MySQLdb as mysql
	user = django_db['USER']
	password = django_db['PASSWORD']
	server = django_db['HOST']
	db = django_db['NAME']
	con = mysql.connect(server, user, password, db, charset='utf8', use_unicode=True)
	cur = con.cursor()
	return con, cur


#  index table of contents text
def index_toc(django_db):
	print("Indexing table of contents.")
	schema = Schema(serial=TEXT(stored=True), topicid=TEXT(stored=True), title=TEXT(stored=True),
	                parent_title=TEXT(stored=True))
	index_folder = "index/"
	import os

	if not os.path.exists(index_folder):
		print "Create folder", index_folder
		os.makedirs(index_folder)

	ix = create_in(index_folder, schema, indexname="toc-index")
	writer = ix.writer()

	con, cur = get_con_by_db(django_db)
	# query = 'select SerialPageID , TopicID, TopicName from Topics where IsLeaf = 1'
	query = 'select SerialPageID , TopicID, TopicName, ParentID from Topics'
	cur.execute(query)
	record_set = cur.fetchall()
	count = 0
	if record_set is not None:
		for record in record_set:
			# try:
			count += 1
			topic_id = record[1]
			serial = str(record[0])
			title = _strip_diacritics(record[2])
			parent_title = get_parent_title(con, cur, record[3])
			parent_title = _strip_diacritics(parent_title)
			if len(parent_title) < 1:
				writer.add_document(serial=serial.decode('utf-8'), topicid=str(topic_id).decode('utf-8'),
				                    title=title)
			else:
				writer.add_document(serial=serial.decode('utf-8'), topicid=str(topic_id).decode('utf-8'),
				                    title=title, parent_title=parent_title)

			print_progress(count)
			# except:
			# 	e = sys.exc_info()
			# 	print "Error:, ", e
			# 	print "index: ", count - 1, "page_serial: ", record[0]
			# 	exit(-1)

	con.close()
	writer.commit()
	print '\n', count, ' TOC records are indexed successfully.'


def get_parent_title(con, cur, parent_id):
	if parent_id is not None:
		query = 'select TopicName from Topics where TopicID = ' + str(parent_id)
		cur.execute(query)
		record_set = cur.fetchall()
		if record_set is not None:
			for record in record_set:
				# print record[0]
				return record[0]

	return u''  # is not unicode; requires any letters !!!!


def get_parent_title_by_topic_id(con, cur, topic_id):
	query = 'select ParentID from Topics where TopicID = ' + str(topic_id)
	cur.execute(query)
	record_set = cur.fetchone()
	parent_id = record_set[0]
	return get_parent_title(con, cur, parent_id)



