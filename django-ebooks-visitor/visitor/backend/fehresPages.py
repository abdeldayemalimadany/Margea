# coding: utf-8

import json
import db


def get_index_item_hits(index_type, item_id):
	result = []
	# url query parameters passed from python are strings
	index_type = int(index_type)

	query = ""
	con, cur = db.get_con()
	if index_type == 1:  # Ayat
		# query = 'SELECT DISTINCT Terms_Ayat.SerialPageID, Topics.TopicName FROM Terms_Ayat INNER JOIN Topics ON Topics.TopicID = Terms_Ayat.TopicID WHERE ID = %s ORDER BY Terms_Ayat.SerialPageID'
		query = 'SELECT DISTINCT Terms_Ayat.SerialPageID, Topics.TopicName FROM Terms_Ayat INNER JOIN Topics ON Topics.TopicID = Terms_Ayat.TopicID WHERE AyaID = %s ORDER BY Terms_Ayat.SerialPageID'
	elif index_type == 2:  # ahadeth_qawlia
		query = 'SELECT DISTINCT Terms_Hadeth.SerialPageID, Topics.TopicName FROM Terms_Hadeth INNER JOIN Topics ON Topics.TopicID = Terms_Hadeth.TopicID WHERE JoinType = 1 AND JoinID = %s ORDER BY Terms_Hadeth.SerialPageID'
	elif index_type == 3:  # ahadeth-fe3lia
		query = 'SELECT DISTINCT Terms_Hadeth.SerialPageID, Topics.TopicName FROM Terms_Hadeth INNER JOIN Topics ON Topics.TopicID = Terms_Hadeth.TopicID WHERE JoinType = 2 AND JoinID = %s ORDER BY Terms_Hadeth.SerialPageID'
	elif index_type == 5:  # kotob
		query = 'SELECT DISTINCT Terms_Topics.SerialPageID, Topics.TopicName FROM Terms_Topics INNER JOIN Topics ON Topics.TopicID = Terms_Topics.TopicID WHERE JoinType = 5 AND JoinedTopicID = %s ORDER BY Terms_Topics.SerialPageID'
	elif index_type == 7:  # aalam
		query = 'SELECT DISTINCT Terms_Topics.SerialPageID, Topics.TopicName FROM Terms_Topics INNER JOIN Topics ON Topics.TopicID = Terms_Topics.TopicID WHERE JoinType = 7 AND JoinedTopicID = %s ORDER BY Terms_Topics.SerialPageID'
	elif index_type == 8:  # ma3lama
		query = 'SELECT DISTINCT Terms_Topics.SerialPageID, Topics.TopicName FROM Terms_Topics INNER JOIN Topics ON Topics.TopicID = Terms_Topics.TopicID WHERE JoinType = 3 AND JoinedTopicID = %s ORDER BY Terms_Topics.SerialPageID'
	elif index_type == 9:  # mostala7at
		query = 'SELECT DISTINCT Terms_Topics.SerialPageID, Topics.TopicName FROM Terms_Topics INNER JOIN Topics ON Topics.TopicID = Terms_Topics.TopicID WHERE JoinType = 9 AND JoinedTopicID = %s ORDER BY Terms_Topics.SerialPageID'
	else:  # More than 9
		# query = "SELECT SerialPageID, Name FROM Terms_Topics WHERE JoinType=%s AND JoinedTopicID=%s order by Name_Sort"
		query = '''SELECT DISTINCT Terms_Topics.SerialPageID, Topics.TopicName
					FROM Terms_Topics INNER JOIN Topics ON Topics.TopicID = Terms_Topics.TopicID
					WHERE JoinType = %s AND JoinedTopicID = %s ORDER BY Terms_Topics.SerialPageID'''

	if index_type >= 1 and index_type <= 9:
		cur.execute(query, (item_id,))
	else:
		cur.execute(query, (index_type, item_id))

	for row in cur.fetchall():
		serial = row[0]
		text = row[1]
		title = db.shorten_text(row[1], 7)
		highlight_code = create_highlight_code(index_type, item_id)
		result.append({'text': text, 'serial': int(serial), 'title': title, 'highlight': highlight_code})

	con.close()
	return json.dumps(result, ensure_ascii=False)


def create_highlight_code(index_type, index_item_id):
	code = ""
	if index_type == 7:  # alaam
		code = 'TermALAM-id-'
	elif index_type == 9:  # Mostala7at
		code = 'TermMost-id-'
	elif index_type == 5:  # kotob
		code = 'BR-id-'
	elif index_type == 8:  # ma3lama
		code = 'ML-id-'
	elif index_type == 10:  # Places الأماكن والبقاع
		code = 'Place-id-'
	elif index_type == 16:  # Feqh Branches الفروع الفقهية
		code = 'FeqhB-id-'
	elif index_type == 17:  # Ejma3at الإجماعات
		code = 'Ejma3at-id-'
	elif index_type == 18:  # Judicial Principles المبادىء القضائية
		code = 'JudPrinc-id-'
	elif index_type == 19:  # Contractual Terms الشروط التعاقدية
		code = 'ContractTerms-id-'
	elif index_type == 21:  # Bodies Institutions الهيئات والمؤسسات
		code = 'Bodies_Inst-id-'
	elif index_type == 22:  # Judicial Systems الأنظمة القضائية
		code = 'JudSys-id-'
	elif index_type == 24:  # Judge القضاة
		code = 'Judge-id-'
	elif index_type == 25:  # Claimant المدعي
		code = 'Claimant-id-'
	elif index_type == 26:  # Respondent المدعى عليه
		code = 'Respondent-id-'
	elif index_type == 27:  # Witnesses الشهود
		code = 'Witnesses-id-'
	elif index_type == 28:  # Experts الخبراء
		code = 'Experts-id-'
	else:
		code = "NOT-EXIST-YET-"

	code += str(index_item_id)  # print code
	return code
