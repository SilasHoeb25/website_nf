from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model, But uses normal Login.
    """
    email = models.EmailField("email address", blank=True)  # Email is optional, can be just username

    # Optional: später kannst du hier zusätzliche Felder hinzufügen
    # z.B. department = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.username

