# -*- coding: utf-8 -*-
from django.conf import settings

READONLY_CODENAME = getattr(settings, 'ADMIN_EXTRAS_READONLY_CODENAME', 'read_only')

# set content types for auto register readonly admin
# for all models use ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT = '__all__'
AUTO_ADMIN_READONLY_CT = getattr(settings, 'ADMIN_EXTRAS_AUTO_ADMIN_READONLY_CT', ())
