# -*- coding: utf-8 -*-
import copy
from django.contrib.auth.models import User, Permission
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes.models import ContentType

from admin_extras import conf


def create_obj(model, defaults, commit=True, **kwargs):
    defaults.update(kwargs)
    obj = model(**defaults)
    if commit:
        obj.save()
    return obj


def create_user(test_case, **kwargs):
    defaults = dict(
        email="rott@joe.com",
        first_name="Joe",
        last_name="Rott",
        is_staff=False,
        is_superuser=False,
    )
    defaults.update(kwargs)
    return User.objects._create_user(**defaults)


def create_staff_user(test_case, **kwargs):
    kwargs.update({'is_staff': True})
    return create_user(test_case, **kwargs)


def create_superuser_user(test_case, **kwargs):
    kwargs.update({'is_superuser': True})
    return create_staff_user(test_case, **kwargs)


def create_flatpage(test_case, **kwargs):
    defaults = dict(
        url='/contacts/',
        title='contacts',
        content='contacts content',
    )
    obj = create_obj(FlatPage, defaults=defaults, **kwargs)
    obj.sites.add(Site.objects.get_current())
    return obj


def add_change_permission(user, model, readonly=False):
    ct = ContentType.objects.get_for_model(model)
    perms = [
        Permission.objects.get(
            content_type=ct,
            codename='%s_%s' % ('change', model._meta.model_name)
        )
    ]
    if readonly:
        perms.append(
            Permission.objects.get(
                content_type=ct,
                codename='%s_%s' % (conf.READONLY_CODENAME, model._meta.model_name)
            ),
        )
    user.user_permissions.add(*perms)


class FakeDefaultPermsOpts(object):
    default_permissions = ('add', 'delete', 'change')


class FakeDefaultPermsWithReadOnlyOpts(object):
    default_permissions = ('add', 'delete', 'change', conf.READONLY_CODENAME)


def get_default_perms(opts):
    return copy.copy(opts.default_permissions)


def get_default_perms_without_readonly(opts):
    opts.default_permissions.remove(conf.READONLY_CODENAME)
    return copy.copy(opts.default_permissions)
