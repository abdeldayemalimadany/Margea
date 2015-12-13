# coding: utf-8

import collections
import json
import MySQLdb
# from db import get_con
# from display.backend.db import get_con
# from ebooks.display.backend import db
from . import db


def get_bookmarks(email):
	bookmarks = []

	con, cursor = db.get_con()

	query = 'SELECT * FROM visitor_bookmark WHERE Email = %s' #   ORDER BY Page

	cursor.execute(query, (email,))

	result = cursor.fetchall()
	num_fields = len(cursor.description)
	field_names = [i[0] for i in cursor.description]
	if result is not None:
		for row in result:
			bookmark = collections.OrderedDict()
			index = 0
			# bookmark['test'] = 'test'
			for field in field_names:
				bookmark[field] = row[index]
				index += 1
				# bookmarks.append({'page': row['ID'], 'title': row[1]})
			bookmarks.append(bookmark)

	con.close()
	return json.dumps(bookmarks, ensure_ascii=False)


def set_bookmark(bookmark_id, email, page_serial, title, search_query):
	con, cur = db.get_con()
	query = 'INSERT INTO visitor_bookmark(bookmark_id, Email, PageSerial, Title, SearchQuery) VALUES(%s, %s, %s, %s, %s)'
	try:

		cur.execute(query, (bookmark_id, email, page_serial, title, search_query))
		con.commit()
		return "success"
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		con.rollback()
		error = "MySQL Error: " + str(e.args[0]) + ", " + str(e.args[1])
		return error


def del_bookmark(bookmark_id):
	con, cur = db.get_con()
	query = 'DELETE FROM visitor_bookmark WHERE bookmark_id = %s'
	try:
		cur.execute(query, (bookmark_id,))
		con.commit()
		return 'success'
	except MySQLdb.Error, e:
		con.rollback()
		error = "MySQL Error: " + e.args[0] + ", " + e.args[1]
		return error

