from django.db import models
from django.utils import timezone


class QuickBooksToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    realm_id = models.CharField(max_length=255)
    expires_in = models.IntegerField()  # token expiry in seconds
    # refresh token expiry in seconds
    x_refresh_token_expires_in = models.IntegerField()
    last_refreshed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"QuickBooks Token for realm {self.realm_id}"


class QuickBooksLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # e.g. 'invoice_created', 'token_refreshed', 'error'
    event_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # e.g. 'success', 'failure'
    message = models.TextField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_type} - {self.status} @ {self.timestamp}"
