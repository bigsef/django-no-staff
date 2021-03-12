from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext as _

from .forms import UserCreationForm
from .models import BaseGroup, Group, User

admin.site.unregister(BaseGroup)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (
            _('Account status'),
            {
                'fields': ('role', 'is_active', 'is_superuser'),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': ('groups', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            },
        ),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': ('role', 'is_active'),
            },
        ),
    )
    readonly_fields = ['date_joined', 'last_login']

    add_form = UserCreationForm
    list_display = (
        '__str__',
        'username',
        'role',
        'is_active',
    )
    list_filter = (
        'is_active',
        'role',
        'groups',
    )
    search_fields = (
        'username',
        'name',
        'email',
    )
    ordering = (
        'name',
        'username',
    )

    def get_readonly_fields(self, request, obj):
        if not request.user.is_superuser:
            self.readonly_fields.append('is_superuser')
        return super().get_readonly_fields(request, obj=obj)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'
