# coding: utf-8

import json
from db import get_con


#  Get list of indexes names and Ids
def get_indexes_names():
	result = []
	query = 'SELECT TermTypeId, TermTypeName FROM termtype WHERE TermTypeID > 0 and isUsed = 1 ORDER BY Rank'
	con, cur = get_con()
	cur.execute(query)
	order = 0
	for row in cur.fetchall():
		result.append({'sort': order, 'type': row[0], 'label': row[1], 'hits': '0'})
		order += 1

	con.close()
	return json.dumps(result, ensure_ascii=False)
