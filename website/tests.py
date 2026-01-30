from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from website.models import Timeslot, Booking
from django.contrib.auth import get_user_model

class BookingAuthTest(TestCase):
    def test_booking_requires_login(self):
        ts = Timeslot.objects.create(
            event_name="Test Event",
            start_at=timezone.now() + timezone.timedelta(days=1),
            end_at=timezone.now() + timezone.timedelta(days=1, hours=1),
            address="Test Address",
            capacity=1,
        )

        response = self.client.post(
            reverse("timeslot_book", args=[ts.id]),
            data={"message": "Test"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


User = get_user_model()

class BookingCapacityTest(TestCase):
    def test_timeslot_capacity_not_exceeded(self):
        user1 = User.objects.create_user(username="u1", password="test")
        user2 = User.objects.create_user(username="u2", password="test")

        ts = Timeslot.objects.create(
            event_name="Test Event",
            start_at=timezone.now() + timezone.timedelta(days=1),
            end_at=timezone.now() + timezone.timedelta(days=1, hours=1),
            address="Test Address",
            capacity=1,
        )

        self.client.login(username="u1", password="test")
        self.client.post(reverse("timeslot_book", args=[ts.id]))

        self.client.logout()
        self.client.login(username="u2", password="test")
        self.client.post(reverse("timeslot_book", args=[ts.id]))

        self.assertEqual(
            Booking.objects.filter(timeslot=ts, status="confirmed").count(),
            1
        )
