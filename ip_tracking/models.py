from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)  # New field
    city = models.CharField(max_length=100, blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp} ({self.city}, {self.country})"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address

