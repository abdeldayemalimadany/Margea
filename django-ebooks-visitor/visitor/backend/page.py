# coding: utf-8

import json
from db import get_con


def get_page(page_serial, index_highlight_code):
	page_serial = str(page_serial)  # convert to ensure data type
	page = 'invalid ID'
	con, cur = get_con()
	query = 'SELECT PageText, SerialPageID, PageID, TopicID, Path FROM Topics_Data WHERE SerialPageID = %s'
	cur.execute(query, (page_serial,))
	path = ''
	result = cur.fetchone()
	if result is not None:
		# arabicStyle = 'text-align: justify;font-size:15pt; font-family: Traditional Arabic; padding-left: 15px;'
		arabicStyle = ''
		# page = '<div dir=rtl id="page_div_%s" style="%s">%s</div>' % (page_serial, arabicStyle, result[0])
		page = '<div id="page_div_%s">%s</div>' % (page_serial, result[0])
		page_serial = result[1]
		number = result[2]
		topic_id = result[3]
		# path = result[4]
		query = 'SELECT FootNoteID, FootNoteText FROM TopicsFootNotes WHERE TopicID = %s AND PageID = %s ORDER BY FootNoteID'
		cur.execute(query, (topic_id, number))
		result = cur.fetchall()
		# footnoteStyle = 'text-align: justify;font-size:11pt; font-family: Traditional Arabic; padding-left: 15px;'
		# footnoteStyle = ''
		if result is not None:
			page += '<br><hr>'
			for row in result:
				# page += '<spin id="hamesh_%d_%d" dir=rtl style="%s">(%d) %s</spin><br>' % (
				page += '<spin class="footnote-text" id="hamesh_%d_%d">(%d) %s</spin><br>' % (
						page_serial, row[0], row[0], row[1])

	con.close()
	page = cleanup_text(page)

	if len(index_highlight_code) > 0:  # if index item exist that needs highlighting
		#  By adding class= at the start, you ensure you do not replace unwanted text
		page = page.replace("class=\"" + index_highlight_code, "class=\"" + "highlight")
		# print ">>> Page is changed, ", index_highlight_code

	return page.encode("UTF-8")


def cleanup_text(result):
	import re
	result = re.sub('\\\\@\\\\@', '<br>', result)
	result = re.sub('\\\\@', '<br>', result)
	result = re.sub('\\n', '<br>', result)
	result = re.sub('/o', '', result) # Exist is Ma3lama
	result = re.sub('font-family: Traditional Arabic;', ' ', result) #  Exist is Ma3lama
	return result

