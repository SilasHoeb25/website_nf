from itertools import count
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Count, F
from django.utils import timezone


class TimeslotStatus(models.TextChoices):
    OPEN = "open", "Open"
    HIDDEN = "hidden", "Hidden"
    CANCELLED = "cancelled", "Cancelled"


class BookingStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"

class TimeslotQuerySet(models.QuerySet):
    def with_confirmed_count(self):
        return self.annotate(
            confirmed_count=Count(
                "bookings",
                filter=Q(bookings__status=BookingStatus.CONFIRMED),
                distinct=True,
            )
        )

    def future(self):
        now = timezone.now()
        return (
            self.filter(end_at__gte=now)           
            .with_confirmed_count()
            .annotate(
                free_spots_db=F("capacity") - F("confirmed_count")
            )
            .order_by("start_at")
        )


class Timeslot(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.TextField(max_length=500, blank=True)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=TimeslotStatus.choices,
        default=TimeslotStatus.OPEN,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(end_at__gt=models.F("start_at")),
                name="timeslot_end_after_start",
            ),
            models.CheckConstraint(
                condition=Q(capacity__gte=1),
                name="timeslot_capacity_gte_1",
            ),
        ]


    def __str__(self) -> str:
        return f"{self.event_name}: {self.start_at:%Y-%m-%d %H:%M}–{self.end_at:%H:%M} ({self.address})"

    @property
    def is_future(self) -> bool:
        return self.end_at >= timezone.now()

    def active_bookings_count(self) -> int:
        return self.bookings.filter(status=BookingStatus.CONFIRMED).count()

    def free_spots(self) -> int:
        return max(0, self.capacity - self.active_bookings_count())
    
    objects = TimeslotQuerySet.as_manager()


class Booking(models.Model):
    timeslot = models.ForeignKey(
        Timeslot,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timeslot_bookings",
    )

    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
        db_index=True,
    )

    booked_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-booked_at"]
        constraints = [
            # A user can only have ONE active booking per timeslot
            models.UniqueConstraint(
                fields=["timeslot", "user"],
                condition=Q(status=BookingStatus.CONFIRMED),
                name="uniq_confirmed_booking_per_user_timeslot",
            ),
        ]
        indexes = [
            models.Index(fields=["timeslot", "status"]),
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.timeslot} ({self.status})"

    def clean(self) -> None:
        # Only validate when creating/confirming
        if self.status != BookingStatus.CONFIRMED:
            return

        if self.timeslot.status != TimeslotStatus.OPEN:
            raise ValidationError("This timeslot is not open for booking.")

        if self.timeslot.end_at < timezone.now():
            raise ValidationError("This timeslot is in the past.")

        # Overbooking guard (best effort; still do atomic check in the booking service/view)
        if self.pk is None and self.timeslot.free_spots() <= 0:
            raise ValidationError("This timeslot is fully booked.")
