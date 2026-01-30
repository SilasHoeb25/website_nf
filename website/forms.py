from datetime import datetime
from django import forms
from django.conf import settings
from django.utils import timezone

from .models import Timeslot


BASE_INPUT_CLASSES = (
    "block w-full rounded-lg border border-slate-300 bg-white "
    "px-3 py-2 text-sm shadow-sm "
    "placeholder:text-slate-400 "
    "focus:border-slate-900 focus:ring-2 focus:ring-slate-900/20"
)

BASE_TEXTAREA_CLASSES = (
    BASE_INPUT_CLASSES + " min-h-[96px]"
)

BASE_SELECT_CLASSES = (
    BASE_INPUT_CLASSES
)

LABEL_CLASSES = "block text-sm font-medium text-slate-700"
HELP_CLASSES = "mt-1 text-xs text-slate-500"
ERROR_CLASSES = "mt-1 text-sm text-red-600"


class TimeslotCreateForm(forms.ModelForm):
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": BASE_INPUT_CLASSES}),
        label="Date",
    )
    start_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={"type": "time", "class": BASE_INPUT_CLASSES}),
        label="Start time",
    )
    end_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={"type": "time", "class": BASE_INPUT_CLASSES}),
        label="End time",
    )

    class Meta:
        model = Timeslot
        fields = [
            "event_name",
            "event_description",
            "address",
            "capacity",
        ]
        widgets = {
            "event_name": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "event_description": forms.Textarea(attrs={"rows": 4, "class": BASE_TEXTAREA_CLASSES}),
            "address": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "capacity": forms.NumberInput(attrs={"class": BASE_INPUT_CLASSES, "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prefill when editing
        if self.instance and self.instance.pk and self.instance.start_at and self.instance.end_at:
            start = self.instance.start_at
            end = self.instance.end_at

            # If USE_TZ=True, make sure we show local date/time to the admin
            if settings.USE_TZ:
                start = timezone.localtime(start)
                end = timezone.localtime(end)

            self.initial.setdefault("date", start.date())
            self.initial.setdefault("start_time", start.time().replace(second=0, microsecond=0))
            self.initial.setdefault("end_time", end.time().replace(second=0, microsecond=0))

    def clean(self):
        cleaned = super().clean()

        date = cleaned.get("date")
        start_time = cleaned.get("start_time")
        end_time = cleaned.get("end_time")

        if not (date and start_time and end_time):
            return cleaned

        start_at = datetime.combine(date, start_time)
        end_at = datetime.combine(date, end_time)

        # If project uses timezone-aware datetimes, convert to aware in current tz
        if settings.USE_TZ:
            tz = timezone.get_current_timezone()
            start_at = timezone.make_aware(start_at, tz)
            end_at = timezone.make_aware(end_at, tz)

        cleaned["start_at"] = start_at
        cleaned["end_at"] = end_at

        if end_at <= start_at:
            raise forms.ValidationError("End must be after start.")

        # Optional: prevent saving events in the past
        if end_at < timezone.now():
            raise forms.ValidationError("Timeslot must be in the future.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_at = self.cleaned_data["start_at"]
        instance.end_at = self.cleaned_data["end_at"]
        if commit:
            instance.save()
        return instance
    

class BookingCreateForm(forms.Form):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": BASE_TEXTAREA_CLASSES,
                "placeholder": "Optional message…",
            }
        ),
        label="Message",
    )
