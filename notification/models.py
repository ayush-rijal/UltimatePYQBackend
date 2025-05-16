# notification/models.py
from django.db import models
from django.utils.timezone import now

class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    count = models.IntegerField()  # total number of categories

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.message}"
