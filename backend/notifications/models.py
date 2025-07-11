from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    recipient_email = models.EmailField()
    customer_name = models.CharField(max_length=100, blank=True, null=True)  # optional
    service_booked = models.CharField(max_length=100, blank=True, null=True)  # optional
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.recipient_email}"
