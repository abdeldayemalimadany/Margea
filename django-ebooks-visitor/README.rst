===============
ebooks-visitor
===============

ebooks-visitor is a Django module to include all backend code for the whole CMSs used.
This app includes the back end code and models only.


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "visitor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'visitor',
    )


2. Include the visitor URLconf in your project urls.py like this::

    url(r'^visitor/', include('visitor.urls')),


3. This app has two managed tables, one for site visitors and the other for bookmarks.


4. Run `python manage.py migrate` to create the django models - if missing, plus visitor models.


6. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage models (you'll need the Admin app enabled).



