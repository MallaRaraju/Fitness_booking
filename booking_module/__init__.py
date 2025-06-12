from booking_module import views
from django.urls import path

urlpatterns = [
    path("book", views.book, name = "book"),
    path("classes", views.fetch_classes, name = "classes"),
    path("bookings", views.fetch_bookings, name = "bookings")
]