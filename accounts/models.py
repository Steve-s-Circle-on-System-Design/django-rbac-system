import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class RoleOptions(models.TextChoices):
    USER = 'USER', 'User'
    ADMIN = 'ADMIN', 'Admin'
    MODERATOR = 'MODERATOR', 'Moderator'


class StatusOptions(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active',
    INACTIVE = 'INACTIVE', 'Inactive',
    SUSPENDED = 'SUSPENDED', 'Suspended',
    PENDING_VERIFICATION = 'PENDING_VERIFICATION', 'Pending_verification'


class ProviderOptions(models.TextChoices):
    LOCAL = 'LOCAL', 'Local',
    GOOGLE = 'GOOGLE', 'Google',
    GITHUB = 'GITHUB', 'Github'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", RoleOptions.ADMIN)
        extra_fields.setdefault("status", StatusOptions.ACTIVE)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser most have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=15,
        choices=RoleOptions.choices,
        default=RoleOptions.USER
    )
    status = models.CharField(
        max_length=30,
        choices=StatusOptions.choices,
        default=StatusOptions.INACTIVE
    )
    provider = models.CharField(
        max_length=30,
        choices=ProviderOptions.choices,
        default=ProviderOptions.LOCAL
    )
    provider_id = models.CharField(
        max_length=100, null=True, blank=True, db_index=True)
    last_login_at = models.DateTimeField(null=True, )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
