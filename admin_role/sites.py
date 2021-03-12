from django.contrib.admin import AdminSite as DAdminSite
from django.contrib.auth import get_user_model

from .forms import AdminAuthenticationForm


class AdminSite(DAdminSite):
    site_header = 'Supervisors Dashboard'
    site_title = 'Dashboard'
    index_title = 'Welcome in Supervisors Dashboard'
    login_form = AdminAuthenticationForm

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.role == get_user_model().ROLES.staff
