from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from core.models import TimeStampedModel
from core.functions import upload_user_directory


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            return ValueError("이메일을 설정해야 합니다")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, max_length=255)
    name = models.CharField(_("name"), max_length=30, blank=True, null=True)
    nickname = models.CharField(
        _("nickname"), max_length=15, unique=True, blank=True, null=True
    )
    profile_img = models.ImageField(
        _("profile image"),
        upload_to=upload_user_directory,
        default="img/default/default_img.jpg",
    )
    self_info = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_superuser = models.BooleanField(_("is_superuser"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.email:
            raise ValueError("email is required.")

        self.profile_img.upload_to = (
            f"profile_img/{self.email}/{self.created_at}/{self.nickname}_img.webp"
        )

        super().save(*args, **kwargs)
