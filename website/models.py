from django.db import models

# booking/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

"""
class SlotStatus(models.TextChoices):
    OPEN = "open", "Open"
    HIDDEN = "hidden", "Hidden"
    CANCELLED = "cancelled", "Cancelled"


class BookingStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class Slot(models.Model):
    # REQUIRED (admin must provide)
    title = models.CharField(max_length=120)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    # OPTIONAL (admin flexibility)
    description = models.TextField(blank=True)
    place = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # Booking logic
    capacity = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=SlotStatus.choices,
        default=SlotStatus.OPEN,
    )

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_at"]
        indexes = [
            models.Index(fields=["start_at"]),
            models.Index(fields=["status", "start_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.start_at}"

    @property
    def confirmed_bookings_count(self) -> int:
        return self.bookings.filter(status=BookingStatus.CONFIRMED).count()

    @property
    def available_spots(self) -> int:
        return max(self.capacity - self.confirmed_bookings_count, 0)

    @property
    def is_bookable(self) -> bool:
        if self.status != SlotStatus.OPEN:
            return False
        now = timezone.now()
        return self.start_at > now and self.confirmed_bookings_count < self.capacity


class Booking(models.Model):
    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            # User cannot book the same slot twice
            models.UniqueConstraint(
                fields=["slot", "user"],
                name="uq_booking_slot_user",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["slot", "status"]),
        ]

    def can_cancel(self) -> bool:
        # User may cancel up to 24h before slot start
        return timezone.now() <= self.slot.start_at - timezone.timedelta(hours=24)

"""