# coding: utf-8

import json
from whoosh.index import open_dir
from whoosh import qparser


# Search for Desktop, Tablet and Mobile in full text of the articles
def search_mobile(words, page_number, option, index_path):
	words = _strip_diacritics(words)
	' '.join(words.split())  # remove multiple spaces
	ix = open_dir(index_path, indexname="text-index")
	# Search options handling
	if option == "statement":  # exact statement
		parser = qparser.QueryParser("page", ix.schema)
		words = '"' + words + '"'
	elif option == "and":
		parser = qparser.QueryParser("page", ix.schema, group=qparser.AndGroup)
	elif option == "or":
		parser = qparser.QueryParser("page", ix.schema, group=qparser.OrGroup)
	elif option == "or-fix":  # with suffix and/or prefix
		parser = qparser.QueryParser("page", ix.schema, group=qparser.OrGroup)
		words = suffix_query(words)
	elif option == "and-fix":
		parser = qparser.QueryParser("page", ix.schema, group=qparser.AndGroup)
		words = suffix_query(words)
	else:
		return json.dumps({'error': 'Unknown search option, ' + option}, ensure_ascii=False)

	query = parser.parse(words)
	final_result = []
	with ix.searcher() as searcher:
		results = searcher.search_page(query, int(page_number), pagelen=10)
		total_count = len(results)
		for hit in results:
			title = hit['title']
			parent_title = hit['parent_title']
			if len(parent_title) > 0:
				full_title = shorten(parent_title, 10) + ' : ' + shorten(title, 10)
			else:
				full_title = shorten(title, 10)

			final_result.append({'text': full_title, 'serial': hit['serial'].encode('utf-8')})

	if option != "statement":
		found_words = words.split(' ')
	else:
		found_words = words

	return json.dumps({'page_number': page_number, 'words': found_words, 'count': total_count, 'result': final_result},
	                  ensure_ascii=False)


def suffix_query(words):  # add suffix or prefix
	suffix_words = ''
	for word in words.split(' '):
		suffix_words += ' *' + word + '*'
	return suffix_words


def _strip_diacritics(text):
	import unicodedata
	# return ''.join([c for c in unicodedata.normalize('NFD', text) \
	#                 if unicodedata.category(c) != 'Mn'])
	return ''.join([c for c in text if unicodedata.category(c) != 'Mn'])


def shorten(string, words_count):
	string = string.strip()
	string = ' '.join(string.split())  # remove duplicate spaces
	words = string.split(' ')
	if len(words) <= words_count:  # no need for shortning
		return string

	count = min(words_count, len(words))
	short_string = ''
	for word in words:
		if count > 0:
			short_string += ' ' + word;
			count -= 1
		else:
			break
	return short_string.strip() + "..."


# Search table of contents leafs
def search_toc(words, index_path):
	words = _strip_diacritics(words)
	' '.join(words.split())  # remove multiple spaces
	ix = open_dir(index_path, indexname="toc-index")
	parser = qparser.QueryParser("title", ix.schema, group=qparser.AndGroup)
	words = suffix_query(words) # prefix and suffix
	query = parser.parse(words)
	final_result = []
	with ix.searcher() as searcher:
		results = searcher.search(query)  # int(page_number), pagelen=10
		total_count = len(results)
		for hit in results:
			title = hit['title']
			parent_title = hit['parent_title']
			full_title = shorten(title, 10)
			if len(parent_title) > 0:
				full_title = shorten(parent_title, 10) + ' : ' + shorten(title, 10)

			final_result.append({'title': full_title,
			                     'serial': hit['serial'].encode('utf-8'), #  "None" if case if not leaf
			                     'topicid': hit['topicid'].encode('utf-8'),
			                     })

	return json.dumps({'count': total_count, 'result': final_result}, ensure_ascii=False)
