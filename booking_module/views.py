from django.views.decorators.csrf import csrf_exempt
from Utils.common_utils import local_aware
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from datetime import datetime, UTC
from django.apps import apps
import json
import sys


@csrf_exempt
def book(request):
    if request.method == 'POST':
        try:
            # fetch API params
            data = json.loads(request.body)

            # loading models
            CourseManagement = apps.get_model('booking_module', 'CourseManagement')
            Booking = apps.get_model('booking_module', 'booking')
            User = apps.get_model('booking_module', 'user')

            course_info = CourseManagement.objects.get(course_id=data["course_id"])

            if course_info.available_seats <= 0:
                return HttpResponse("No slots available", status=404)

            user_info = User.objects.get(email=data["email"])

            # Create booking
            Booking.objects.create(booking_date=datetime.now(UTC), status='booked',
                                   course_management_id=course_info.id, user_id=user_info.id)

            # Decrease seat count
            course_info.available_seats-=1
            course_info.save()

            return HttpResponse("booking successful")

        except CourseManagement.DoesNotExist:
            return HttpResponse("No such course available", status=404)
        except User.DoesNotExist:
            return HttpResponse("No such user available", status=404)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Exception occurred in book: {str(e)} at line no. {str(exc_tb.tb_lineno)}")
            return None
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)

def fetch_bookings(request):
    if request.method == 'GET':
        try:
            # fetch API params
            params = request.GET.dict()
            user_id = int(params.get("user_id"))
            _timezone = params.get("timezone", 'UTC')

            # loading models
            Booking = apps.get_model('booking_module', 'booking')
            booking_info = Booking.objects.filter(user_id=user_id).select_related('course_management')

            response_json = []
            for booking in booking_info:
                booking_details = {'start_time': local_aware(booking.course_management.slot.start_time, _timezone),
                                   'end_time': local_aware(booking.course_management.slot.end_time, _timezone),
                                   'instructor_name': booking.course_management.instructor.name,
                                   'course_name': booking.course_management.course.course_name}
                response_json.append(booking_details)

            return JsonResponse({'response': response_json})
        except Booking.DoesNotExist:
            return JsonResponse({"error": "no bookings were done"}, status=404)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Exception occurred in fetch_bookings: {str(e)} at line no. {str(exc_tb.tb_lineno)}")
            return None
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)

def fetch_classes(request):
    try:
        if request.method == 'GET':
            # fetch API params
            params = request.GET.dict()
            _timezone = params.get("timezone", 'UTC')

            # loading models
            CourseManagement = apps.get_model('booking_module', 'CourseManagement')

            course_info = list(CourseManagement.objects.select_related('course', 'instructor', 'slot').values(
                'instructor__name',
                'available_seats',
                'course__course_name', 'course__description',
                'slot__start_time', 'slot__end_time'))

            # converting to localtime
            for index, row in enumerate(course_info):
                for column in ['slot__start_time', 'slot__end_time']:
                    row[column] = local_aware(row[column], _timezone)
                course_info[index] = row

            return JsonResponse({"response": course_info})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Exception occurred in fetch_classes: {str(e)} at line no. {str(exc_tb.tb_lineno)}")
        return None
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)