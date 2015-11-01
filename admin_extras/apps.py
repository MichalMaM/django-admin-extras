from django.apps import AppConfig
from django.contrib.auth import management
from django.utils.translation import ugettext_lazy as _

from .decorators import add_readonly_to_builtin_permissions


class AdminExtrasConfig(AppConfig):
    name = 'admin_extras'
    verbose_name = _("Admin extras")


# inject readonly permission to builtin permissions
management._get_builtin_permissions = add_readonly_to_builtin_permissions(management._get_builtin_permissions)
