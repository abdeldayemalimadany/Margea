# coding: utf-8

import page
from ..models import BookFootNotes, BookPages
from django.db.models import Max


def get_page(book_id, page_id):
	books = BookPages.objects.filter(BookID=book_id, PageId=page_id)
	book = books[0]
	footnotes = BookFootNotes.objects.filter(BookID=book_id, PageId=page_id)
	foots = ['(' + str(fn.FootNoteId) + ') ' + fn.FootNoteText + '<br>' for fn in footnotes]
	page_text = book.PageText_FootNotesOnly
	if len(foots) > 0:
		page_text += '<hr>' + ''.join(foots)

	page_text = page.cleanup_text(page_text)
	max_page = BookFootNotes.objects.filter(BookID=book_id).aggregate(Max('PageId'))['PageId__max']
	result = {'book': book.BookID, 'max': max_page,
	          'page': str(book.PageId), 'text': page_text}
	import json
	return json.dumps(result, ensure_ascii=False)

