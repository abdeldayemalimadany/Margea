from django.db import models

# Create your models here.


class Zabayen(models.Model):
	def __unicode__(self):
		return self.Email
	Email = models.CharField(max_length=40)
	Pass = models.CharField(max_length=40)
	Salt = models.CharField(max_length=40)

	class Meta:
		# db_table = 'Zabayen'
		verbose_name_plural = "Visitors Data"
		ordering = ['Email']


class Bookmark(models.Model):
	def __unicode__(self):
		return self.Title
	bookmark_id = models.CharField(max_length=100, primary_key=True) # Now, django will not automatically add an ID
	Email = models.CharField(max_length=40)
	Title = models.CharField(max_length=100)
	PageSerial = models.CharField(max_length=10)
	SearchQuery = models.CharField(max_length=100)

	class Meta:
		# db_table = 'Bookmark'
		verbose_name_plural = "Visitors Bookmarks"
		ordering = ['Title']

class TopicsData(models.Model):
	def __unicode__(self):  # for Python 2.7
		return self.Path

	SerialPageID = models.IntegerField()
	PageID = models.IntegerField()
	TopicID = models.CharField(max_length=15)
	Path = models.CharField(max_length=150)
	PageText = models.TextField()

	class Meta:
		db_table = 'Topics_Data'
		managed = False  # no database table creation or deletion operations will be performed for this model
		verbose_name_plural = "Display Data, [Topics_Data table]"
		ordering = ['SerialPageID']


class Topics(models.Model):
	def __unicode__(self):  # for Python 2.7
		return self.TopicName

	TopicID = models.CharField(max_length=100)
	TopicName = models.CharField(max_length=100)
	IsLeaf = models.IntegerField()
	SerialPageID = models.IntegerField()

	class Meta:
		db_table = 'Topics'
		managed = False  # no database table creation or deletion operations will be performed for this model
		verbose_name_plural = "Tree Data [Topics table]"
		ordering = ['SerialPageID']


class Terms(models.Model):  # definitions inside display
	def __unicode__(self):  # for Python 2.7
		return self.TermName

	TermID = models.IntegerField()
	TermTypeID = models.IntegerField()
	TermName = models.CharField(max_length=150)
	TermDefinitions = models.TextField()

	class Meta:
		db_table = 'Terms'
		managed = False  # no database table creation or deletion operations will be performed for this model
		verbose_name_plural = "Terms A3lam [Terms table]"
		ordering = ['TermName']


class BooksReferences(models.Model):
	def __unicode__(self):  # for Python 2.7
		return self.Name

	ID = models.IntegerField()
	Name = models.CharField(max_length=200)
	Notes = models.TextField()

	class Meta:
		db_table = 'Books_References'
		managed = False  # no database table creation or deletion operations will be performed for this model
		verbose_name_plural = "Terms Book References [Books_References table]"
		ordering = ['Name']


# Fahares models are not done as Fahares is going to be overhauled and re-implemented

############################################################
#Ma3lama


# class Books(models.Model):
# 	BookID = models.TextField(primary_key=True)
# 	BookName = models.TextField()
#
# 	def __unicode__(self):  # for Python 2.7
# 		return self.BookName
#
# 	class Meta:
# 		db_table = 'Books'
# 		managed = False  # no table creation or deletion
# 		verbose_name_plural = "Books [Books table]"
# 		ordering = ['BookName']


class BookPages(models.Model):
	PageId = models.IntegerField(primary_key=True)
	BookID = models.TextField()
	PageText = models.TextField()
	PageText_FootNotesOnly = models.TextField()


	def __unicode__(self):  # for Python 2.7
		return self.PageId

	class Meta:
		db_table = 'BookPages'
		managed = False  # no table creation or deletion
		verbose_name_plural = "Books Pages [BooksPages table]"
		ordering = ['PageId']


class BookFootNotes(models.Model):
	FootNoteId = models.IntegerField(primary_key=True)
	BookID = models.TextField()
	PageId = models.IntegerField()
	FootNoteText = models.TextField()

	def __unicode__(self):  # for Python 2.7
		return self.FootNoteText

	class Meta:
		db_table = 'BookFootNotes'
		managed = False  # no table creation or deletion
		verbose_name_plural = "Books FootNotes [BookFootNote table]"
		ordering = ['FootNoteId']

