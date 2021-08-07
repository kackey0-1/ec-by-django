import re

from django.core.validators import RegexValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=150, blank=False)
    postal_code = models.CharField(_('postal code'), max_length=8,)
    address = models.CharField(_('address'), max_length=255, blank=True)
    phone = models.CharField(_('phone'), max_length=13, blank=True,)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),)
    login_count = models.IntegerField(_('login count'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def post_login(self):
        """ログイン後処理"""
        self.login_count += 1
        self.save()

    def activate_user(self):
        self.is_active = True
        self.save()

    def send_verify_mail(self, current_site):
        subject = 'Activate your account.'
        message = render_to_string('mail/user/confirmation_instructions.html', {
            'user': self,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(self.email)),
            'token': default_token_generator.make_token(self), })
        self._send_email(subject, message)

    def send_reset_password_mail(self, current_site):
        subject = 'Reset your password.'
        message = render_to_string('mail/user/password_reset.html', {
            'user': self,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(self.email)),
            'token': default_token_generator.make_token(self), })
        self._send_email(subject, message)

    def _send_email(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta(object):
        db_table = 'user'



