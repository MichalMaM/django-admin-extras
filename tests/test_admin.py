from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage

from admin_extras.admin import ReadOnlyMixin

from .utils import (
    create_staff_user,
    create_superuser_user,
    create_flatpage,
    add_change_permission,
)

from nose import tools


class TestReadOnlyAdmin(TestCase):

    def setUp(self):
        super(TestReadOnlyAdmin, self).setUp()
        self.model_for_read_only = FlatPage
        self.rf = RequestFactory()
        self.staff_user = create_staff_user(
            self,
            username='john',
            email='john@john.com',
            password='top_secret',
        )
        self.superuser = create_superuser_user(
            self,
            username='joe',
            email='joe@joe.com',
            password='top_secret',
        )
        self.flatpage = create_flatpage(
            self,
            content='page'
        )

    def test_readonly_staff_user_has_excluded_spec_actions(self):
        add_change_permission(self.staff_user, self.model_for_read_only, readonly=True)
        admin_class = admin.site._registry[self.model_for_read_only].__class__
        admin_instance = admin_class(self.model_for_read_only, admin.site)
        url = reverse('admin:flatpages_flatpage_changelist')
        request = self.rf.get(url)
        request.user = self.staff_user
        for action in ReadOnlyMixin.drop_actions:
            tools.assert_not_in(action, admin_instance.get_actions(request))

    def test_readonly_staff_user_get_change_flatpage(self):
        add_change_permission(self.staff_user, self.model_for_read_only, readonly=True)
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        response = c.get(url)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(200, response.status_code)

    def test_readonly_staff_user_cannot_change_flatpage(self):
        new_content = '%s 2' % self.flatpage.content
        add_change_permission(self.staff_user, self.model_for_read_only, readonly=True)
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        post_data = dict(
            _save='save',
            url=self.flatpage.url,
            title=self.flatpage.title,
            template_name=self.flatpage.template_name or '',
            sites=self.flatpage.sites.all()[0].pk,
            content=new_content,
        )
        response = c.post(url, data=post_data)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(self.flatpage.content, FlatPage.objects.get(pk=self.flatpage.pk).content)
        self.assertRedirects(response, url)

    def test_superuser_has_all_actions(self):
        admin_class = admin.site._registry[self.model_for_read_only].__class__
        admin_instance = admin_class(self.model_for_read_only, admin.site)
        url = reverse('admin:flatpages_flatpage_changelist')
        request = self.rf.get(url)
        request.user = self.superuser
        for action in ReadOnlyMixin.drop_actions:
            tools.assert_in(action, admin_instance.get_actions(request))

    def test_superuser_get_change_flatpage(self):
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.superuser.username, password='top_secret'))
        response = c.get(url)
        tools.assert_true(self.superuser.is_staff)
        tools.assert_true(self.superuser.is_active)
        tools.assert_true(self.superuser.is_superuser)
        tools.assert_true(self.superuser.is_authenticated())
        tools.assert_equals(200, response.status_code)

    def test_superuser_user_can_change_flatpage(self):
        new_content = '%s 2' % self.flatpage.content
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        redir_url = reverse('admin:flatpages_flatpage_changelist')
        c = Client()
        tools.assert_true(c.login(username=self.superuser.username, password='top_secret'))
        post_data = dict(
            _save='save',
            url=self.flatpage.url,
            title=self.flatpage.title,
            template_name=self.flatpage.template_name or '',
            sites=self.flatpage.sites.all()[0].pk,
            content=new_content,
        )
        response = c.post(url, data=post_data)
        tools.assert_true(self.superuser.is_staff)
        tools.assert_true(self.superuser.is_active)
        tools.assert_true(self.superuser.is_authenticated())
        tools.assert_equals(new_content, FlatPage.objects.get(pk=self.flatpage.pk).content)
        self.assertRedirects(response, redir_url)

    def test_staff_user_with_perm_has_all_actions(self):
        add_change_permission(self.staff_user, self.model_for_read_only)
        admin_class = admin.site._registry[self.model_for_read_only].__class__
        admin_instance = admin_class(self.model_for_read_only, admin.site)
        url = reverse('admin:flatpages_flatpage_changelist')
        request = self.rf.get(url)
        request.user = self.staff_user
        for action in ReadOnlyMixin.drop_actions:
            tools.assert_in(action, admin_instance.get_actions(request))

    def test_staff_user_with_perm_get_change_flatpage(self):
        add_change_permission(self.staff_user, self.model_for_read_only)
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        response = c.get(url)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(200, response.status_code)

    def test_staff_user_with_perm_can_change_flatpage(self):
        new_content = '%s 2' % self.flatpage.content
        add_change_permission(self.staff_user, self.model_for_read_only)
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        redir_url = reverse('admin:flatpages_flatpage_changelist')
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        post_data = dict(
            _save='save',
            url=self.flatpage.url,
            title=self.flatpage.title,
            template_name=self.flatpage.template_name or '',
            sites=self.flatpage.sites.all()[0].pk,
            content=new_content,
        )
        response = c.post(url, data=post_data)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(new_content, FlatPage.objects.get(pk=self.flatpage.pk).content)
        self.assertRedirects(response, redir_url)

    def test_staff_user_without_perms_cannot_view_change_flatpage(self):
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        response = c.get(url)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(403, response.status_code)

    def test_staff_user_without_perms_cannot_change_flatpage(self):
        new_content = '%s 2' % self.flatpage.content
        url = reverse('admin:flatpages_flatpage_change', args=(self.flatpage.id,))
        c = Client()
        tools.assert_true(c.login(username=self.staff_user.username, password='top_secret'))
        post_data = dict(
            _save='save',
            url=self.flatpage.url,
            title=self.flatpage.title,
            template_name=self.flatpage.template_name or '',
            sites=self.flatpage.sites.all()[0].pk,
            content=new_content,
        )
        response = c.post(url, data=post_data)
        tools.assert_true(self.staff_user.is_staff)
        tools.assert_true(self.staff_user.is_active)
        tools.assert_true(self.staff_user.is_authenticated())
        tools.assert_equals(self.flatpage.content, FlatPage.objects.get(pk=self.flatpage.pk).content)
        tools.assert_equals(403, response.status_code)
