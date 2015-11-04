import logging

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


from .decorators import cache_result
from .admin import ReadOnlyMixin
from . import conf

logger = logging.getLogger(__name__)


def ct_str_natural_key(data):
    return "%s.%s" % data


def get_models():
    dj_models = apps.get_models()
    if conf.AUTO_ADMIN_READONLY_CT == '__all__':
        return dj_models
    out = []
    for m in dj_models:
        opts = ContentType.objects._get_opts(m, for_concrete_model=True)
        str_natural_key = ct_str_natural_key((opts.app_label, opts.model_name,))
        if str_natural_key in conf.AUTO_ADMIN_READONLY_CT:
            out.append(m)
    return out


def add_readonly_to_model_admin(model):
    opts = admin.site._registry[model].__class__
    # if ReadOnlyMixin is not in ancestors create new admin class
    if not issubclass(opts, ReadOnlyMixin):
        # create new admin class from old class and readonly mixin
        opt_new = type('ReadOnly%s' % opts.__name__, (ReadOnlyMixin, opts), {})
        admin.site.unregister(model)
        admin.site.register(model, opt_new)


@cache_result()
def add_readonly_to_models_admin():
    for model in get_models():
        if model in admin.site._registry.keys():
            add_readonly_to_model_admin(model)
