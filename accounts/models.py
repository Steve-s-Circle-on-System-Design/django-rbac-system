from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid


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


class OTPStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    USED = 'USED', 'Used'
    EXPIRED = 'EXPIRED', 'Expired'


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


class OTPVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otpstatus = models.CharField(choices=OTPStatus.choices, default=OTPStatus.PENDING)


class PasswordReset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class EmailLog(models.Model):
    class EmailStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        OPENED = "opened", "Opened"
        CLICKED = "clicked", "Clicked"
        FAILED = "failed", "Failed"
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="email_logs", null=True, blank=True)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=EmailStatus.choices, default=EmailStatus.PENDING)
    message_id = models.CharField(max_length=255)
    error = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_id} | {self.subject} | {self.status}"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=36)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=255)
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} | {self.action}"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    mime_type = models.CharField(max_length=100)
    cloudinary_public_id = models.CharField(max_length=255)
    secure_url = models.CharField(max_length=500)
    format = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
