# coding: utf-8

import json
from db import get_con


def get_serial(topicID):
	pageSerial = 1

	query = 'SELECT SerialPageID FROM TopicsData WHERE TopicID = %s ORDER BY SerialPageID LIMIT 1'

	con, cur = get_con()
	cur.execute(query, (topicID,))

	result = cur.fetchone()
	if result is not None:
		pageSerial = result[0]

	con.close()
	return json.dumps({'serial': pageSerial}, ensure_ascii=False)
