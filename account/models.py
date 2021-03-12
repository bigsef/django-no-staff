from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group as BaseGroup, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = Choices('staff', 'moderator', 'customer')
    USERNAME_VALIDATOR = RegexValidator(
        regex='^[a-z_]*$',
        message=_('Enter a valid Username consisting of lowercase letters or underscores.'),
        code='invalid',
    )

    # region Model Attribute
    name = models.CharField('full name', max_length=75, blank=True)
    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Required. 50 characters or fewer. only contain lowercase letters or underscores.',
        validators=[USERNAME_VALIDATOR],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
        help_text='Required. valid email must be provided to use when contact with user.',
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
    )

    role = StatusField(
        'user role',
        choices_name='ROLES',
        default=ROLES.moderator,
        blank=True,
        db_index=True,
        help_text=_('Select user role in site. based on role will decide where user can log into.'),
    )
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Designates whether this user should be treated as active.\
            Unselect this instead of deleting accounts.',
    )
    is_verified = models.BooleanField(
        'Has Verified Account', default=False, help_text='Designates whether this user has completed sign up process.'
    )

    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    # endregion

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('authentication Accounts')

    def __str__(self) -> str:
        return self.name if self.name else str(self.username)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def update_last_login(self, commit: bool = True) -> None:
        """
        update last_login field with now datetime and save update
        :parameter commit: if i want to override save behavior
        :return: None
        """
        self.last_login = timezone.now()
        if commit:
            self.save()


class Group(BaseGroup):
    class Meta:
        proxy = True
        app_label = "account"
