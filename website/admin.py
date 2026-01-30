from django.contrib import admin
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime

from .models import Timeslot, Booking, BookingStatus


class TimeslotSplitAdminForm(forms.ModelForm):
    # UI-only fields (not stored directly in DB)
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),  # calendar
        help_text="Select the date of the timeslot.",
    )
    from_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={"type": "time"}),  # time picker
        help_text="Start time.",
    )
    to_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={"type": "time"}),  # time picker
        help_text="End time.",
    )

    class Meta:
        model = Timeslot
        # We hide start_at/end_at from the form and use our split fields instead
        exclude = ("start_at", "end_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # When editing an existing timeslot, pre-fill date/from/to from start_at/end_at
        if self.instance and self.instance.pk:
            start_local = timezone.localtime(self.instance.start_at)
            end_local = timezone.localtime(self.instance.end_at)
            self.initial["date"] = start_local.date()
            self.initial["from_time"] = start_local.time().replace(second=0, microsecond=0)
            self.initial["to_time"] = end_local.time().replace(second=0, microsecond=0)

    def clean(self):
        cleaned = super().clean()

        d = cleaned.get("date")
        t_from = cleaned.get("from_time")
        t_to = cleaned.get("to_time")

        if not d or not t_from or not t_to:
            return cleaned

        if t_to <= t_from:
            raise ValidationError("End time must be after start time.")

        # Combine date + time into aware datetimes using current timezone
        tz = timezone.get_current_timezone()
        start_dt = timezone.make_aware(datetime.combine(d, t_from), tz)
        end_dt = timezone.make_aware(datetime.combine(d, t_to), tz)

        # Store them on the model instance so save() persists them
        self.instance.start_at = start_dt
        self.instance.end_at = end_dt

        return cleaned


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("user", "status", "message", "booked_at", "cancelled_at")
    readonly_fields = ("booked_at", "cancelled_at")
    autocomplete_fields = ("user",)
    show_change_link = True


@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    form = TimeslotSplitAdminForm

    list_display = ("start_at", "end_at", "address", "capacity", "status", "confirmed_count", "free_spots")
    list_filter = ("status",)
    search_fields = ("address",)
    date_hierarchy = "start_at"
    ordering = ("-start_at",)

    inlines = [BookingInline]

    def confirmed_count(self, obj: Timeslot) -> int:
        return obj.bookings.filter(status=BookingStatus.CONFIRMED).count()
    confirmed_count.short_description = "Confirmed"

    def free_spots(self, obj: Timeslot) -> int:
        return obj.free_spots()
    free_spots.short_description = "Free spots"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("timeslot", "user", "status", "booked_at", "cancelled_at")
    list_filter = ("status", "timeslot__status")
    search_fields = ("user__username", "user__email", "timeslot__address")
    autocomplete_fields = ("timeslot", "user")
    readonly_fields = ("booked_at",)
    ordering = ("-booked_at",)
