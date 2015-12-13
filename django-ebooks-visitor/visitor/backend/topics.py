# coding: utf-8

import json
from db import get_con
from search import shorten

# get the body, and head in one call, no styling
# show which one is the active one
# Topics table


def browse_tree(topic_id):
	con, cur = get_con()
	topic_id = int(topic_id)
	if topic_id == 1:
		# special ID means that is root tree view
		root = get_root_elements()
		if len(root) == 1:
			# one head element
			head = root
			body = get_tree_kids(head[0]['TopicID'])
		else:
			# multi head elements
			head = []
			body = root
	else:
		# Just legal and valid ID got from database
		body = get_tree_kids(topic_id)
		head = get_tree_head(topic_id)

	return json.dumps({'head': head, 'body': body}, ensure_ascii=False)


# sometimes it is one element, and in others it is multi elements just like Margea
def get_root_elements():
	con, cur = get_con()
	query = 'select TopicID, TopicName, IsLeaf, SerialPageID from Topics where parentID is NULL ' \
	        'or ParentID = 0 order by SortID'
	cur.execute(query)
	result = cur.fetchall()
	root = []
	if result is not None:
		for row in result:
			short_title = shorten(row[1], 15)
			root.append({'TopicID': row[0], 'TopicName': short_title, 'IsLeaf': row[2], 'SerialPageID': row[3]})

	con.close()
	return root



# Valid topicID must be sent
def get_tree_kids(topicID):
	con, cur = get_con()
	from search import shorten
	query = 'select TopicID, TopicName, IsLeaf, SerialPageID from Topics where parentID = %s order by SortID'
	cur.execute(query, (topicID, ))
	result = cur.fetchall()
	body = []
	body_count = 0
	if result is not None:
		for row in result:
			body_count += 1
			short_title = shorten(row[1], 15)
			body.append({'TopicID': row[0], 'TopicName': short_title, 'IsLeaf': row[2], 'SerialPageID': row[3]})

	con.close()
	return body


def get_tree_head(topicID):
	con, cur = get_con()
	query = 'select TopicID, TopicName, Path, IsLeaf from Topics where TopicID = %s'
	cur.execute(query, (topicID,))
	row = cur.fetchone()
	head = []
	if row is not None:
		path = row[2]
		# print 'path is ', path
		for tid in path.split('/'):
			cur.execute(query, (tid,))
			row = cur.fetchone()
			if row is not None:
				head.append({'TopicID': row[0], 'TopicName': shorten(row[1], 25), 'IsLeaf': row[3]})
	return head


def browse_tree_by_serial(serial):
	# get topic id
	con, cur = get_con()
	# query = 'select TopicID from Topics where SerialPageID = %s'
	query = 'SELECT TopicID FROM Topics_Data WHERE SerialPageID = %s'
	cur.execute(query, (serial, ))
	row = cur.fetchone()
	if row is not None:
		topicID = row[0]
		con.close()
		return browse_tree(topicID)
	else:
		return "Not Found"
