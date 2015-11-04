from django.test import TestCase
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.conf import settings

from admin_extras.utils import get_models, apps, add_readonly_to_model_admin
from admin_extras.admin import ReadOnlyMixin
from admin_extras import conf

from nose import tools


class TestReadOnlyTools(TestCase):

    def setUp(self):
        super(TestReadOnlyTools, self).setUp()
        self.model_for_read_only = FlatPage

    def test_get_models_for_content_types_spec_in_settings(self):
        tools.assert_equals(
            [ContentType.objects.get_by_natural_key(*settings.ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT[0].split('.')).model_class()],
            get_models()
        )

    def test_get_all_models_if_spec_in_conf(self):
        old_value = conf.AUTO_ADMIN_READONLY_CT
        conf.AUTO_ADMIN_READONLY_CT = '__all__'
        tools.assert_equals(apps.get_models(), get_models())
        conf.AUTO_ADMIN_READONLY_CT = old_value

    def test_get_empty_models_if_spec_in_conf(self):
        old_value = conf.AUTO_ADMIN_READONLY_CT
        conf.AUTO_ADMIN_READONLY_CT = ()
        tools.assert_equals([], get_models())
        conf.AUTO_ADMIN_READONLY_CT = old_value

    def test_auto_register_readonly_admin_for_spec_content_types(self):
        opts = admin.site._registry[self.model_for_read_only].__class__
        tools.assert_equals(opts.__name__, "ReadOnlyFlatPageAdmin")
        tools.assert_true(issubclass(opts, (ReadOnlyMixin, FlatPageAdmin)))

    def test_no_register_new_readonly_admin_for_readonly_admin(self):
        add_readonly_to_model_admin(self.model_for_read_only)
        opts = admin.site._registry[self.model_for_read_only].__class__
        tools.assert_equals(opts.__name__, "ReadOnlyFlatPageAdmin")
        tools.assert_true(issubclass(opts, (ReadOnlyMixin, FlatPageAdmin)))
