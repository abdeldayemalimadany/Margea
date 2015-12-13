from django.http import HttpResponse
from backend import bookmark, users
from visitor.backend import page, serial, definition, fehres, fehresList, topics
from visitor.backend import search, fehresPages, ma3lama
from django.conf import settings


def query(request, name, def_value="0"):
	try:
		value = request.GET[name]
	except:
		value = def_value
	return value


def query_str(request, name, def_value=""):
	try:
		value = request.GET[name]
	except:
		value = def_value
	return value

# Create your views here.
# def query(request, name, def_value="0"):
# 	try:
# 		return request.GET[name]
# 	except:  # MultiValueDictKeyError as e
# 		return def_value
# 	# return value


def signup(request):
	output = users.add_user(query(request, "email"), query(request, "password"), query(request, "password2"))
	return HttpResponse(output)


def signin(request):
	mail = query(request, "email")
	response = users.sign_in(mail, query(request, "password"))
	return response

###############################
# Bookmarks


def get_bookmarks(request):
	# db = query(request, "db")
	output = "[]"
	if users.is_logged_in(request):
		output = bookmark.get_bookmarks(users.get_logged_email(request))

	return HttpResponse(output)


def set_bookmark(request):
	# db = query(request, "db")
	output = "Authentication required"
	if users.is_logged_in(request):
		email = users.get_logged_email(request)
		output = bookmark.set_bookmark(query(request, "bookmark_id"), email,
		                               query(request, "pageSerial"), query(request, "title"), query(request, "query"))

	return HttpResponse(output)


def del_bookmark(request):
	# db = query(request, "db")
	output = "Authentication required"
	if users.is_logged_in(request):
		# email = users.get_logged_email(request, db)
		# query(request, "db"),
		output = bookmark.del_bookmark(query(request, "id"))

	return HttpResponse(output)

#####################################################################


def get_page(request):
	return HttpResponse(page.get_page(query(request, "pageSerial"), query_str(request, "indexHighlightCode")))


def get_serial(request):
	return HttpResponse(serial.get_serial(query(request, "topicID")))


def get_definition(request):
	return HttpResponse(definition.get_definition(query(request, "type"), query(request, "id")))


def get_topics(request):  # Tree data
	topic = query(request, "topic", "-1")
	serial_no = query(request, "serial", "-1")
	if serial_no == "-1":  # def value
		return HttpResponse(topics.browse_tree(topic))
	else:
		return HttpResponse(topics.browse_tree_by_serial(serial_no))


def get_search(request):
	return HttpResponse(search.search_mobile(query(request, "word"), query(request, "page"),
											query(request, "option"), settings.WHOOSH_INDEX_PATH))


def get_index(request):
	return HttpResponse(fehres.get_index(query(request, "type")))


def get_index_pages(request):
	return HttpResponse(fehresPages.get_index_item_hits(query(request, "type"), query(request, "id")))


def get_index_list(request):
	return HttpResponse(fehresList.get_indexes_names())

# Ma3lama Views
def get_ma3lama_books(request):
	result = ma3lama.get_page(query(request, "book", None),
	                          query(request, "page", "1"))
	return HttpResponse(result)


def get_search_toc(request):
	return HttpResponse(search.search_toc(query(request, "word"), settings.WHOOSH_INDEX_PATH))
