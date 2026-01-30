from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    # Booking / Timeslots
    path("booking/", views.booking, name="timeslots"),
    path("booking/create/", views.timeslot_create, name="timeslot_create"),
    path("booking/<int:pk>/", views.timeslot_book, name="timeslot_book"),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path("booking/<int:pk>/edit/", views.timeslot_edit, name="timeslot_edit"),


    #cancel endpoints
    path("my_bookings/<int:booking_id>/cancel/", views.booking_cancel, name="booking_cancel"),
    path("booking/<int:pk>/cancel/", views.timeslot_cancel, name="timeslot_cancel"),

]


