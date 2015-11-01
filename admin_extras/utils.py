import logging
from django.contrib.contenttypes.models import ContentType

try:
    from django.apps import apps
except ImportError:  # django < 1.7
    from django.db.models.loading import get_models as dj_get_models
else:
    dj_get_models = apps.get_models

from . import conf

logger = logging.getLogger(__name__)


def ct_str_natural_key(contenttype):
    return "%s.%s" % contenttype.natural_key()


def get_models():
    dj_models = dj_get_models()
    if conf.AUTO_ADMIN_READONLY_CT == '__all__':
        return dj_models
    out = []
    for m in dj_models:
        try:
            ct = ContentType.objects.get_for_model(m)
        except Exception:
            logger.error("Can not get content_type for model", extra={'model': m}, exc_info=True)
            continue
        str_natural_key = ct_str_natural_key(ct)
        if str_natural_key in conf.AUTO_ADMIN_READONLY_CT:
            out.append(m)
    return out
