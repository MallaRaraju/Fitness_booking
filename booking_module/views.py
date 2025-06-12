from django.views.decorators.csrf import csrf_exempt
from Utils.common_utils import local_aware
from django.shortcuts import HttpResponse
from Utils.Logger import LoggerUtility
from django.http import JsonResponse
from datetime import datetime, UTC
from django.apps import apps
import json
import sys

logger = LoggerUtility(module='booking_module')

@csrf_exempt
def book(request):
    if request.method == 'POST':
        try:
            logger.log(f"1. {request.method}-book: API called")
            # fetch API params
            data = json.loads(request.body)

            logger.log(f"2. {request.method}-book: Loading DB models")
            CourseManagement = apps.get_model('booking_module', 'CourseManagement')
            Booking = apps.get_model('booking_module', 'booking')
            User = apps.get_model('booking_module', 'user')

            course_info = CourseManagement.objects.get(course_id=data["course_id"])

            if course_info.available_seats <= 0:
                logger.log(f"3. {request.method}-book: No slots are available")
                return HttpResponse("No slots available", status=404)

            logger.log(f"3. {request.method}-book: slots are available")
            user_info = User.objects.get(email=data["email"])

            logger.log(f"4. {request.method}-book: creating record in bookings")
            Booking.objects.create(booking_date=datetime.now(UTC), status='booked',
                                   course_management_id=course_info.id, user_id=user_info.id)

            logger.log(f"5. {request.method}-book: updating seat count")
            course_info.available_seats-=1
            course_info.save()

            return HttpResponse("booking successful")

        except CourseManagement.DoesNotExist:
            logger.log(f"#. {request.method}-book: Exception occurred no such course found", level='error')
            return HttpResponse("No such course available", status=404)
        except User.DoesNotExist:
            logger.log(f"#. {request.method}-book: Exception occurred no such user found", level='error')
            return HttpResponse("No such user available", status=404)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.log(f"Exception occurred in book: {str(e)} at line no. {str(exc_tb.tb_lineno)}",
                       level='error')
            return HttpResponse(status=400)
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)

def fetch_bookings(request):
    if request.method == 'GET':
        try:
            logger.log(f"1. {request.method}-booking: API bookings")
            # fetch API params
            params = request.GET.dict()
            user_id = int(params.get("user_id"))
            _timezone = params.get("timezone", 'UTC')

            logger.log(f"2. {request.method}-booking: Loading DB models")
            Booking = apps.get_model('booking_module', 'booking')
            booking_info = Booking.objects.filter(user_id=user_id).select_related('course_management')

            logger.log(f"3. {request.method}-booking: formating response and adjusting timezone")
            response_json = []
            for booking in booking_info:
                booking_details = {'start_time': local_aware(booking.course_management.slot.start_time, _timezone),
                                   'end_time': local_aware(booking.course_management.slot.end_time, _timezone),
                                   'instructor_name': booking.course_management.instructor.name,
                                   'course_name': booking.course_management.course.course_name}
                response_json.append(booking_details)

            return JsonResponse({'response': response_json})
        except Booking.DoesNotExist:
            logger.log(f"#. {request.method}-booking: Exception occurred no bookings found")
            return JsonResponse({"error": "no bookings were done"}, status=404)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.log(f"#. {request.method}-book: Exception occurred in {str(e)} at line no. {str(exc_tb.tb_lineno)}",
                       level='error')
            return HttpResponse(status=400)
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)

def fetch_classes(request):
    try:
        if request.method == 'GET':
            # fetch API params
            logger.log(f"1. {request.method}-classes: API called")
            params = request.GET.dict()
            _timezone = params.get("timezone", 'UTC')

            logger.log(f"2. {request.method}-classes: Loading DB models")
            CourseManagement = apps.get_model('booking_module', 'CourseManagement')

            logger.log(f"3. {request.method}-classes: fetching course related information")
            course_info = list(CourseManagement.objects.select_related('course', 'instructor', 'slot').values(
                'instructor__name',
                'available_seats',
                'course__course_name', 'course__description',
                'slot__start_time', 'slot__end_time'))

            logger.log(f"4. {request.method}-classes: updating time based on timezone")
            for index, row in enumerate(course_info):
                for column in ['slot__start_time', 'slot__end_time']:
                    row[column] = local_aware(row[column], _timezone)
                course_info[index] = row

            return JsonResponse({"response": course_info})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.log(f"#. {request.method}-classes: Exception occurred in fetch_classes: {str(e)} at line no. "
                   f"{str(exc_tb.tb_lineno)}", level='error')
        return HttpResponse(status=400)
    else:
        return JsonResponse({"error": "Unsupported method"}, status=415)