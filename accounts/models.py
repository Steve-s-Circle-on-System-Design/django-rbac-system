from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField()
    email = models.EmailField(unique=True)
    username = models.EmailField(max_length=50)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    class RoleOptions(models.TextChoices):
        USER = 'USER', 'User'
        ADMIN = 'ADMIN', 'Admin'
        MODERATOR = 'MODERATOR', 'Moderator'

    role = models.CharField(
        max_length=15,
        choices=RoleOptions.choices,
        default=RoleOptions.USER
    )
    class StatusOptions(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active',
        INACTIVE = 'INACTIVE', 'Inactive',
        SUSPENDED = 'SUSPENDED', 'Suspended',
        PENDING_VERIFICATION = 'PENDING_VERIFICATION', 'Pending_verification'

    status = models.CharField(
        max_length=30,
        choices=StatusOptions.choices,
        default=StatusOptions.INACTIVE
    )
    class ProviderOptions(models.TextChoices):
        LOCAL = 'LOCAL', 'Local',
        GOOGLE = 'GOOGLE', 'Google',
        GITHUB = 'GITHUB', 'Github'

    provider = models.CharField(
        max_length=30,
        choices=ProviderOptions.choices,
        default=ProviderOptions.LOCAL
    )
    provider_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    last_login_at = models.DateTimeField(null=True, )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username
