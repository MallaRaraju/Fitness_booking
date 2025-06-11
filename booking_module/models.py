from django.db import models

# Master: Instructors
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

# Master: Slots
class Slot(models.Model):
    slot_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

# Master: Courses
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    total_intake = models.IntegerField()

# Transaction: Users
class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()

# Master: Course Management (Offering)
class CourseManagement(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    available_seats = models.IntegerField()

# Transaction: Bookings
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_management = models.ForeignKey(CourseManagement, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='booked')  # e.g., booked, cancelled
