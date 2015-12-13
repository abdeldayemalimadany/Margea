from django.contrib import admin
from .models import *

# Register your models here.

# Managed models
admin.site.register(Bookmark)
admin.site.register(Zabayen)
#Display objects
admin.site.register(TopicsData)
admin.site.register(Topics)
admin.site.register(Terms)
admin.site.register(BooksReferences)
