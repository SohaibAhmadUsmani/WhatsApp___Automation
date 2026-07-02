from email.policy import default
from django.db import models

# Create your models here.
class WhatsAppMessage(models.Model):
    STATUS_CHOICES=[('pending','Pending'),('sent','Sent'),('failed','Failed')]
    phone_number=models.CharField(max_length=15, help_text=("Enter Ph No with Country Code "))
    message=models.TextField()
    sent_at=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    sent_at=models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES , default='pending')
    error_message=models.TextField(blank=True, null=True)
    scheduled_time=models.DateTimeField()
    def __str__ (self):
        return f"{self.phone_number}-{self.scheduled_time}"