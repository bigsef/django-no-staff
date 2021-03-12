from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username or not email:
            raise ValueError(_('The given username or email must be set.'))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        password = password if password else self.make_random_password(length=9)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_moderator(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'moderator')
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_staff(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'staff')
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'staff')
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError('backend must be a dotted import path string (got %r).' % backend)
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    def check_username_availability(self, username: str) -> bool:
        if username:
            qs = self.filter(username=username)
            return not qs.exists()
        return True

    def check_email_availability(self, email: str) -> bool:
        if email:
            qs = self.filter(email=email)
            return not qs.exists()
        return True
