from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from admin_extras.admin import ReadOnlyMixin

from nose import tools


class TestReadOnlyAdmin(TestCase):

    def setUp(self):
        super(TestReadOnlyAdmin, self).setUp()
        self.model_for_read_only = FlatPage
        self.rf = RequestFactory()
        self.user = User.objects.create(
            username='john',
            email='john@john.com',
            password='top_secret',
            is_staff=True
        )

    def test_auto_register_readonly_admin_for_spec_content_types(self):
        opts = admin.site._registry[self.model_for_read_only].__class__
        tools.assert_equals(opts.__name__, "ReadOnlyFlatPageAdmin")
        tools.assert_true(issubclass(opts, (ReadOnlyMixin, FlatPageAdmin)))
