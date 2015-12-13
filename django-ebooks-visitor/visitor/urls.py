from django.conf.urls import url

from . import views

# ORDERED, BE CAREFUL
urlpatterns = [
	url(r'^signup', views.signup),
	url(r'^signin', views.signin),
	url(r'^get_bookmarks', views.get_bookmarks),
	url(r'^set_bookmark', views.set_bookmark),
	url(r'^del_bookmark', views.del_bookmark),
	#########
	url(r'^page$', views.get_page),
	url(r'^topics', views.get_topics),  # critical to put fehresPages before fehres !!!
	url(r'^fehresPages', views.get_index_pages),
	url(r'^fehresList', views.get_index_list),
	url(r'^fehres', views.get_index),
	url(r'^searchToc', views.get_search_toc),
	url(r'^search', views.get_search),
	url(r'^definition', views.get_definition),
	url(r'^serial', views.get_serial),
	#Ma3lama Requests
	url(r'^ma3lama_books$', views.get_ma3lama_books),


]
