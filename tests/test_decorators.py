import copy

from django.test import TestCase

from admin_extras.decorators import add_readonly_to_builtin_permissions
from admin_extras import conf

from .utils import (
    get_default_perms,
    get_default_perms_without_readonly,
    FakeDefaultPermsOpts,
    FakeDefaultPermsWithReadOnlyOpts,
)

from nose import tools

decorated_get_default_perms = add_readonly_to_builtin_permissions(get_default_perms)
decorated_get_default_perms_without_readonly = add_readonly_to_builtin_permissions(get_default_perms_without_readonly)


class TestDecorators(TestCase):

    def test_add_readonly_to_builtin_permissions(self):
        default_permissions = copy.copy(list(FakeDefaultPermsOpts.default_permissions))
        tools.assert_equals(
            default_permissions + [conf.READONLY_CODENAME],
            decorated_get_default_perms(FakeDefaultPermsOpts),
        )

    def test_does_not_add_readonly_to_builtin_permissions_if_is_there(self):
        default_permissions = copy.copy(FakeDefaultPermsWithReadOnlyOpts.default_permissions)
        tools.assert_equals(
            default_permissions,
            decorated_get_default_perms(FakeDefaultPermsWithReadOnlyOpts),
        )

    def test_does_not_raise_exception_during_cleanup_of_add_readonly_to_builtin_permissions(self):
        default_permissions = copy.copy(list(FakeDefaultPermsOpts.default_permissions))
        tools.assert_equals(
            default_permissions,
            decorated_get_default_perms_without_readonly(FakeDefaultPermsOpts),
        )
