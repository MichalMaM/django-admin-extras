from django.test import TestCase

from nose import tools


def formfield_for_dbfield(obj, db_field, **kwargs):
    return obj, db_field, kwargs


class TestUtils(TestCase):
    pass
