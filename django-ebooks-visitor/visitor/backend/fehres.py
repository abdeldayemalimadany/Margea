# coding: utf-8

import json
import db


# Get Index list of items per index type
def get_index(index_type):
	result = []
	# url query parameters passed from python are strings
	index_type = str(index_type)
	querySource = {
		#'1': 'SELECT Name, ID FROM Terms_Ayat ORDER BY SoraNO, AyaNO',  # ayat
		'1': 'SELECT DISTINCT Name_Shamla AS Name, AyaID AS ID FROM Terms_Ayat ORDER BY AyaID',  # ayat
		'2': 'SELECT Name, ID FROM Terms_Hadeth WHERE JoinType = 1 and ID=JoinID ORDER BY Name_Sort',  # ahadeth_qawlia
		'3': 'SELECT Name, ID FROM Terms_Hadeth WHERE JoinType = 2 and ID=JoinID ORDER BY Name_Sort',  # ahadeth-fe3lia
		'5': 'SELECT Name, ID FROM Books_References ORDER BY Name_Sort',  # kotob
		'7': 'SELECT TermName, TermID FROM Terms WHERE TermTypeID = 7 ORDER BY Name_Sort',  # aalam
		'8': 'SELECT BookName, BookID FROM Books ORDER BY Name_Sort',  # ma3lama
		'9': 'SELECT TermName, TermID FROM Terms WHERE TermTypeID = 9 ORDER BY Name_Sort',  # mostala7at
		# New indexes
		'10': 'SELECT Name, ID FROM Places ORDER BY Name_Sort',
		'16': 'SELECT TopicName, TopicID FROM TopicsFeqh ORDER BY SortID',
		'17': 'SELECT Name, ID FROM Ejma3at ORDER BY Name_Sort',
		'18': 'SELECT Name, ID FROM JudicialPrinciples ORDER BY Name_Sort',
		'19': 'SELECT Name, ID FROM ContractualTerms ORDER BY Name_Sort',
		'21': 'SELECT Name, ID FROM Bodies_Institutions ORDER BY Name_Sort',
		'22': 'SELECT TopicName, TopicID FROM topicsjudicialsystems ORDER BY SortID',
		'24': 'SELECT Name, ID FROM Judge ORDER BY Name_Sort',
		'25': 'SELECT Name, ID FROM Claimant ORDER BY Name_Sort',
		'26': 'SELECT Name, ID FROM Respondent ORDER BY Name_Sort',
		'27': 'SELECT Name, ID FROM Witnesses ORDER BY Name_Sort',
		'28': 'SELECT Name, ID FROM Experts ORDER BY Name_Sort',
	}
	con, cur = db.get_con()
	cur.execute(querySource[index_type])
	for row in cur.fetchall():
		text = row[0]
		ID = row[1]
		result.append({'text': text, 'id': ID, 'type': index_type})

	con.close()
	return json.dumps(result, ensure_ascii=False)
