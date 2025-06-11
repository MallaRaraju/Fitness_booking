from tkinter.font import names

from django.urls import path
from booking_module import views

urlpatterns = [
    path("book", views.book, name = "book"),
    path("classes", views.fetch_classes, name = "classes"),
    path("bookings", views.fetch_bookings, name = "bookings")
]