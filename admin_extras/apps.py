from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import management

from .decorators import add_readonly_to_builtin_permissions
from .utils import add_readonly_to_models_admin
from . import conf


class AdminExtrasConfig(AppConfig):
    name = 'admin_extras'
    verbose_name = _("Admin extras")

    def ready(self):
        # call auto register readonly admins
        if conf.AUTO_ADMIN_READONLY_CT:
            add_readonly_to_models_admin()


# inject readonly permission to builtin permissions
management._get_builtin_permissions = add_readonly_to_builtin_permissions(management._get_builtin_permissions)
