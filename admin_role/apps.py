from django.contrib.admin.apps import AdminConfig as DAdminConfig


class AdminConfig(DAdminConfig):
    default_site = 'admin_role.sites.AdminSite'
