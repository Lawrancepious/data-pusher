# data_app/models.py
from django.db import models
from django.utils.crypto import get_random_string


class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(
        max_length=255, unique=True, default=get_random_string
    )
    website = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = get_random_string(32)
        super().save(*args, **kwargs)


class Destination(models.Model):
    account = models.ForeignKey(
        Account, related_name="destinations", on_delete=models.CASCADE
    )
    url = models.URLField()
    http_method = models.CharField(max_length=10)
    headers = models.TextField()  # Store headers as a comma-separated string
