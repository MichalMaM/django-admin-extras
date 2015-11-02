from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_permission_codename
from django.utils.translation import ugettext_lazy as _

from . import conf


class ReadOnlyMixin(object):
    read_only_per_codename = conf.READONLY_CODENAME
    drop_actions = ('delete_selected')

    def has_add_permission(self, request):
        if self.has_read_only_permission(request):
            return False
        return super(ReadOnlyMixin, self).has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if self.has_read_only_permission(request, obj):
            return False
        return super(ReadOnlyMixin, self).has_delete_permission(request, obj)

    def has_read_only_permission(self, request, obj=None):
        # ignore if usperuser has red only permition
        if request.user.is_superuser:
            return False
        opts = self.opts
        codename = get_permission_codename(self.read_only_per_codename, opts)
        ret = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return ret

    def get_actions(self, request):
        actions = super(ReadOnlyMixin, self).get_actions(request)
        if self.has_read_only_permission(request):
            for action in self.drop_actions:
                action in actions and actions.remove(action)
        return actions

    def disable_editing(self):
        # disable list editable
        self.list_editable = ()
        # self.raw_id_fields = ()

    def get_readonly_fields(self, request, obj=None):
        if self.has_read_only_permission(request, obj):
            self.disable_editing()
        return super(ReadOnlyMixin, self).get_readonly_fields(request, obj)

    def change_view(self, request, *args, **kwargs):
        if request.method == 'POST' and self.has_read_only_permission(request):
            msg = _('You have no permissions for this changes')
            self.message_user(request, msg, messages.ERROR)
            return HttpResponseRedirect(request.get_full_path())
        return super(ReadOnlyMixin, self).change_view(request, *args, **kwargs)


class ReadOnlyModelAdmin(ReadOnlyMixin, admin.ModelAdmin):
    pass
