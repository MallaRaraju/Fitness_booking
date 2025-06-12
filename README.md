# 🧘 Fitness Booking App

A Django-based web application to manage fitness class bookings, course availability, and user data using SQLite3 and Python 3.12.

---

## 📦 Requirements

- Python 3.12+
- SQLite3 (included with Python)
- Linux / WSL (Windows Subsystem for Linux)

---

## 🚀 Quick Start

> **_NOTE:_** change the log folder path in configuration>constants.py-->'Log_Folder'.


Follow the steps below to set up, and run the application.

### 1. (Optional) Modify Fixtures
Update fixture files in booking_module/fixtures/ if you want to pre-load additional data.

### 2. Run Setup Script
Make the script executable and run it:
```
chmod +x setup.sh
./setup.sh
```
### 3. Verify Setup
Visit the link below in your browser:<br>
[Django admin dashboard](http://127.0.0.1:8000/admin/login/?next=/admin/)<br><br>
If you see the Django admin dashboard, the application is up and running!

### 4. Checkout DB schema
To see the relations and DB design view the db_schema.png image in the repo.

### 5. API's
API views are implemented in booking_module/views.py

#### a. Get List of Classes
Returns all available classes/courses (supports timezone adjustment).
```commandline
curl --location 'http://127.0.0.1:8000/booking/classes?timezone=Asia%2FKolkata'
```

#### b. Get User Bookings
Returns all bookings made by a specific user.
```commandline
curl --location 'http://127.0.0.1:8000/booking/bookings?user_id=1&timezone=Asia%2FDubai'
```
#### c. Book a Class
Books a class for a user if available. Requires email and course_id in request body.
```commandline
curl --location 'http://127.0.0.1:8000/booking/book' \
     --header 'Content-Type: application/json' \
     --data-raw '{
        "email": "rahul@example.com",
        "course_id": 3
        }'
```
### 6. Test run
To run the test scenarios, run the command
```commandline
python manage.py test
```

> **_NOTE:_**  Every operation mentioned are supposed to run from, inside the 'Fitness_booking' folder.
