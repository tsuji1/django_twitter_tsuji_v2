from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(BaseUserManager):
    use_in_migratons = True

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validater = ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,
        help_text=(
            'Required,15 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validater],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    self_introduction = models.CharField(
        _('self introduction'), max_length=512, blank=True, help_text='15 characters or fewer')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
