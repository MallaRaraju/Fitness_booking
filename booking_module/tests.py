from booking_module.models import User, CourseManagement, Booking, Course, Instructor, Slot
from django.test import TestCase, Client
from django.utils.timezone import now

class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            full_name="Test User",
            email="test@example.com",
            gender="male",
            age=25,
            password="testpass"
        )
        self.instructor = Instructor.objects.create(
            name="John Doe",
            age=35,
            gender="male"
        )

        self.slot = Slot.objects.create(
            slot_name="Morning Batch",
            start_time="06:00:00",
            end_time="07:00:00"
        )

        self.course = Course.objects.create(
            course_name="Yoga Basics",
            cost=500,
            description="Introductory Yoga class",
            total_intake=30
        )
        self.course_mgmt = CourseManagement.objects.create(
            slot_id=1,  # Replace with actual FK ID from your fixture
            course_id=1,
            instructor_id=1,
            available_seats=5
        )

    def test_successful_booking(self):
        response = self.client.post("/booking/book", data={
            "email": self.user.email,
            "course_id": self.course_mgmt.course_id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("booking successful", response.content.decode())

    def test_booking_with_no_seats(self):
        self.course_mgmt.available_seats = 0
        self.course_mgmt.save()
        response = self.client.post("/booking/book", data={
            "email": self.user.email,
            "course_id": self.course_mgmt.course_id
        }, content_type='application/json')
        self.assertNotIn("booking successful", response.content.decode())

    def test_classes_api(self):
        response = self.client.get("/booking/classes?timezone=Asia/Kolkata")
        self.assertEqual(response.status_code, 200)

    def test_bookings_api(self):
        Booking.objects.create(
            user_id=self.user.id,
            course_management_id=self.course_mgmt.id,
            status='booked',
            booking_date=now()
        )
        response = self.client.get(f"/booking/bookings?user_id={self.user.id}&timezone=Asia/Kolkata")
        self.assertEqual(response.status_code, 200)
        self.assertIn("start_time", response.content.decode())

    def test_invalid_user_email(self):
        response = self.client.post("/booking/book", data={
            "email": "invalid@example.com",
            "course_id": self.course_mgmt.course_id
        }, content_type='application/json')
        self.assertNotEqual(response.status_code, 200)

    def test_invalid_course_id(self):
        response = self.client.post("/booking/book", data={
            "email": self.user.email,
            "course_id": 9999
        }, content_type='application/json')
        self.assertNotEqual(response.status_code, 200)

    def test_get_instead_of_post(self):
        response = self.client.get("/booking/book")
        self.assertEqual(response.status_code, 415)

    def test_invalid_timezone(self):
        response = self.client.get("/booking/classes?timezone=Invalid/Zone")
        self.assertEqual(response.status_code, 400)

    def test_missing_post_data(self):
        response = self.client.post("/booking/book", data={}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
