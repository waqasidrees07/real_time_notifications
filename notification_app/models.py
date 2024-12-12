from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import notification_status


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)

    def __str__(self):
        return self.email


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    status = models.CharField(choices=notification_status, max_length=255, default="unread")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.message[:15]}"
