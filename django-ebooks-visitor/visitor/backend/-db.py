import MySQLdb as mysql
from django.conf import settings


def getCon():
	django_db = settings.DATABASES['default']
	user = django_db['USER']
	password = django_db['PASSWORD']
	server = django_db['HOST']
	db = django_db['NAME']
	con = mysql.connect(server, user, password, db, charset='utf8', use_unicode=True)
	cur = con.cursor()
	return con, cur


def shorten_text(text, wordsCount):
	wordArray = text.split(' ')
	if (len(wordArray) <= wordsCount):
		return text  # no shortening needed
	newText = ' '.join(wordArray[0:wordsCount])
	return newText + "..."


def strip_html(page):
	import re
	return re.sub('<[^<]+?>|&nbsp;', ' ', page)  # strip html tags

