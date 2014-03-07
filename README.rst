Django Tagging Translated
=========================

Registers the ``Tag`` model of
`django-tagging <https://github.com/brosner/django-tagging>`_ for
`django-hvad` and extends the Tag admin.


Installation
------------

Prerequisites:

* Django
* django-tagging
* django-hvad

If you want to install the latest stable release from PyPi::

    $ pip install django-tagging-translated

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-tagging-translated.git#egg=tagging_translated

Add ``tagging_translated`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'tagging_translated',
    )

Run the South migrations::

    ./manage.py migrate tagging_translated


Usage
-----

You can simply created and edit your tags and translations in the Django admin.

Roadmap
-------

Check the issue tracker on github for milestones and features to come.
