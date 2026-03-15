from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Role Flags
    is_regular_admin = models.BooleanField(default=False)
    is_department_admin = models.BooleanField(default=False)

    # FIX FOR THE ERRORS:
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Unique name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Unique name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username