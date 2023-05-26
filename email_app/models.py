from django.db import models
import uuid

class Email(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    recipient = models.EmailField()
    is_opened = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


