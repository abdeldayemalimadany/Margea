# coding: utf-8

import json
from db import get_con
import page


def get_definition(definition_type, definition_ids_str):
	# definition_title = 'invalid ID'
	# definition_text = 'invalid ID'
	if definition_type == 'TermALAM':
		query = 'SELECT TermName, TermDefinitions FROM Terms WHERE TermTypeID = 7 AND TermID = %s'
	elif definition_type == 'TermMost':
		query = 'SELECT TermName, TermDefinitions FROM Terms WHERE TermTypeID = 9 AND TermID = %s'
	elif definition_type == 'BR':
		query = 'SELECT Name, Notes FROM Books_References WHERE ID = %s'
	#Added By Abdeldayem
	elif definition_type == 'JudSys':
		query = 'SELECT TopicName AS Name, TopicText AS Notes FROM TopicsJudicialSystems WHERE TopicID = %s'
	elif definition_type == 'Bodies_Inst':
		query = 'SELECT Name, Notes FROM Bodies_Institutions WHERE ID = %s'
	elif definition_type == 'JudPrinc':
		query = 'SELECT Name, Notes FROM JudicialPrinciples WHERE ID = %s'
	elif definition_type == 'ContractTerms':
		query = 'SELECT Name, Notes FROM ContractualTerms WHERE ID = %s'
	elif definition_type == 'Place':
		query = 'SELECT Name, Notes FROM Places WHERE ID = %s'
	else:
		query = None

	# It is a set of IDs
	definition_ids = str(definition_ids_str).split(",")
	final_result = []
	if query is None:
		return json.dumps(final_result, ensure_ascii=False)

	con, cur = get_con()
	for def_id in definition_ids:
		cur.execute(query, (def_id,))
		result = cur.fetchone()
		if result is not None:
			definition_title = result[0]
			definition_text = page.cleanup_text(result[1])
			final_result.append({'title': definition_title, 'text': definition_text})

	con.close()
	return json.dumps(final_result, ensure_ascii=False)
