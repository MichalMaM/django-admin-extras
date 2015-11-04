Django-admin-extras v. 0.0.1
############################

.. _description:

**Django admin extras** is django application that contains useful extras for django admin.

.. _requirements:

Requirements
============

- python >= 2.7
- Django >= 1.7


Setup
=====

- Add 'admin_extras' to INSTALLED_APPS ::

    INSTALLED_APPS += ( 'admin_extras', )


Use django-admin-extras
=======================

#) Read only admin:

    - Use ReadOnlyModelAdmin as base class ::

        from django.contrib import admin
        from admin_extras.admin import ReadOnlyModelAdmin

        class MyAdmin(ReadOnlyModelAdmin):
            list_display = ('title', 'content',)

        admin.site.register(MyModel, MyAdmin)

    - Use ReadOnlyMixin ::

        from django.contrib import admin
        from admin_extras.admin import ReadOnlyMixin

        class MyAdmin(admin.ModelAdmin):
            list_display = ('title', 'content',)

        class ReadOnlyMyAdmin(ReadOnlyMixin, MyAdmin):
            pass

        admin.site.register(MyModel, ReadOnlyMyAdmin)

#) Read only admin auto register:

    The easiest way is setup setting ``ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT`` in ``settings.py``::

	ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT = (
	    'flatpages.flatpage',
	)


Settings
========

**ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT** - content types natural keys (string representation) of models that will be used for auto register new read only admin.
By default `()`.

Example: `settings.py` ::

    ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT = (
        'flatpages.flatpage',
        'myapp.mymodel',
    )

**ADMIN_EXTRAS_READONLY_CODENAME** - code name for read only permission, It will be inject to django default permissions. By default `read_only`.


License
=======

Licensed under a `BSD license`.
