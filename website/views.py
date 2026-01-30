from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from .forms import BookingCreateForm, TimeslotCreateForm
from .models import Booking, BookingStatus, Timeslot, TimeslotStatus


def home(request):
    if request.headers.get("HX-Request") == "true":
        return render(request, "partials/_home_content.html")
    return render(request, "home.html")


def about(request):
    if request.headers.get("HX-Request") == "true":
        return render(request, "partials/_about_content.html")
    return render(request, "about.html")


def booking(request):
    qs = Timeslot.objects.future()

    # Hide cancelled events for non-staff users
    if not request.user.is_authenticated or not request.user.is_staff:
        qs = qs.filter(status=TimeslotStatus.OPEN)

    timeslots = qs

    my_booking_id_by_timeslot = {}
    if request.user.is_authenticated:
        my_booking_id_by_timeslot = dict(
            Booking.objects.filter(
                user=request.user,
                status=BookingStatus.CONFIRMED,
                timeslot_id__in=timeslots.values_list("id", flat=True),
            ).values_list("timeslot_id", "id")
        )

    return render(
        request,
        "booking/timeslots.html",
        {
            "timeslots": timeslots,
            "my_booking_id_by_timeslot": my_booking_id_by_timeslot,
        },
    )


@login_required
def timeslot_book(request, pk: int):
    if request.method == "POST":
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    ts = Timeslot.objects.select_for_update().get(pk=pk)

                    if ts.status != TimeslotStatus.OPEN:
                        raise ValidationError("This timeslot is not open for booking.")
                    if not ts.is_future:
                        raise ValidationError("This timeslot is in the past.")

                    confirmed = Booking.objects.filter(
                        timeslot=ts, status=BookingStatus.CONFIRMED
                    ).count()
                    if confirmed >= ts.capacity:
                        raise ValidationError("This timeslot is fully booked.")

                    if Booking.objects.filter(
                        timeslot=ts, user=request.user, status=BookingStatus.CONFIRMED
                    ).exists():
                        raise ValidationError("You already booked this timeslot.")

                    Booking.objects.create(
                        timeslot=ts,
                        user=request.user,
                        status=BookingStatus.CONFIRMED,
                        message=form.cleaned_data.get("message", ""),
                    )

                messages.success(request, "Booking created!")
                return redirect("timeslots")

            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        ts = get_object_or_404(Timeslot, pk=pk)
        form = BookingCreateForm()

    if request.method == "POST":
        ts = get_object_or_404(Timeslot, pk=pk)

    return render(request, "booking/timeslot_book.html", {"timeslot": ts, "form": form})


@staff_member_required
def timeslot_create(request):
    if request.method == "POST":
        form = TimeslotCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Timeslot created!")
            return redirect("timeslots")
    else:
        form = TimeslotCreateForm()

    return render(request, "booking/timeslot_create.html", {"form": form})



@staff_member_required
def timeslot_edit(request, pk: int):
    ts = get_object_or_404(Timeslot, pk=pk)

    if request.method == "POST":
        form = TimeslotCreateForm(request.POST, instance=ts)
        if form.is_valid():
            form.save()
            messages.success(request, "Timeslot updated!")
            return redirect("timeslots")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = TimeslotCreateForm(instance=ts)

    return render(request, "booking/timeslot_edit.html", {"form": form, "timeslot": ts})



@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(
            user=request.user,
            timeslot__end_at__gte=timezone.now(),
            status__in=[BookingStatus.CONFIRMED, BookingStatus.CANCELLED],
        )
        .select_related("timeslot")
        .order_by("timeslot__start_at")
        )
    return render(
        request,
        "booking/my_bookings.html",
        {"bookings": bookings},
    )



@login_required
@require_POST
@transaction.atomic
def booking_cancel(request, booking_id: int):
    booking = get_object_or_404(
        Booking.objects.select_for_update().select_related("timeslot"),
        pk=booking_id,
    )

    # user can cancel only own booking (staff could be allowed too if you want)
    if booking.user_id != request.user.id and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed.")

    if booking.status == BookingStatus.CANCELLED:
        messages.info(request, "Booking already cancelled.")
        return redirect("timeslots")

    booking.status = BookingStatus.CANCELLED
    booking.cancelled_at = timezone.now()
    booking.save(update_fields=["status", "cancelled_at"])

    messages.success(request, "Booking cancelled.")
    return redirect("timeslots")


@staff_member_required
@require_POST
@transaction.atomic
def timeslot_cancel(request, pk: int):
    ts = get_object_or_404(Timeslot.objects.select_for_update(), pk=pk)

    if ts.status == TimeslotStatus.CANCELLED:
        messages.info(request, "Timeslot already cancelled.")
        return redirect("timeslots")

    ts.status = TimeslotStatus.CANCELLED
    ts.save(update_fields=["status"])

    # cancel all confirmed bookings in that timeslot
    Booking.objects.filter(timeslot=ts, status=BookingStatus.CONFIRMED).update(
        status=BookingStatus.CANCELLED,
        cancelled_at=timezone.now(),
    )

    messages.success(request, "Timeslot cancelled (all bookings cancelled).")
    return redirect("timeslots")



@staff_member_required
@require_POST
@transaction.atomic
def timeslot_cancel(request, pk: int):
    ts = get_object_or_404(Timeslot.objects.select_for_update(), pk=pk)

    if ts.status == TimeslotStatus.CANCELLED:
        messages.info(request, "Event ist bereits abgesagt.")
        return redirect("timeslots")

    # Cancel the timeslot itself
    ts.status = TimeslotStatus.CANCELLED
    ts.save(update_fields=["status"])

    # Cancel all confirmed bookings for that timeslot
    Booking.objects.filter(timeslot=ts, status=BookingStatus.CONFIRMED).update(
        status=BookingStatus.CANCELLED,
        cancelled_at=timezone.now(),
    )

    messages.success(request, "Event wurde abgesagt.")
    return redirect("timeslots")
