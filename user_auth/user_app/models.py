from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Adding mobile and verified fields
    mobile = models.CharField(max_length=16, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    # Fixing clash with reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_app_users',  # Add a custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_app_users',  # Add a custom related_name
        blank=True
    )

    def __str__(self):
        return self.username
