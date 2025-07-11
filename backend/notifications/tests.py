from django.test import TestCase
from django.utils import timezone
from django.core import mail
from .models import Notification, NotificationTemplate


class NotificationModelTest(TestCase):
    def test_create_notification(self):
        notification = Notification.objects.create(
            title="Test Notification",
            message="Test message",
            recipient_email="test@example.com",
            sent=True,
            sent_at=timezone.now()
        )
        self.assertEqual(notification.recipient_email, "test@example.com")
        self.assertTrue(notification.sent)
        self.assertIsNotNone(notification.sent_at)


class NotificationTemplateModelTest(TestCase):
    def test_create_notification_template(self):
        template = NotificationTemplate.objects.create(
            name="booking_template",
            title="Car Wash Booking Confirmed!",
            body="Hello {{user}}, your booking for {{service}} has been received. See you soon!"
        )
        self.assertEqual(template.name, "booking_template")
        self.assertIn("{{user}}", template.body)
        self.assertIn("{{service}}", template.body)


class CarwashBookingNotificationTest(TestCase):
    def setUp(self):
        # Create a reusable template
        self.template = NotificationTemplate.objects.create(
            name="booking_template",
            title="Car Wash Booking Confirmed!",
            body="Hello {{user}}, your booking for {{service}} has been received. See you soon!"
        )

    def test_send_booking_email(self):
        user_name = "Brian"
        service = "Full Exterior Wash"
        recipient_email = "brian@gmail.com"

        # Replace placeholders
        personalized_message = self.template.body.replace("{{user}}", user_name).replace("{{service}}", service)

        # Simulate sending email
        mail.send_mail(
            subject=self.template.title,
            message=personalized_message,
            from_email="cwash3001@gmail.com",
            recipient_list=[recipient_email],
            fail_silently=False
        )

        # Save Notification
        Notification.objects.create(
            title=self.template.title,
            message=personalized_message,
            recipient_email=recipient_email,
            sent=True,
            sent_at=timezone.now()
        )

        # Assert email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(service, mail.outbox[0].body)
        self.assertIn(user_name, mail.outbox[0].body)

        # Assert Notification saved
        notification = Notification.objects.get(recipient_email=recipient_email)
        self.assertEqual(notification.message, personalized_message)
