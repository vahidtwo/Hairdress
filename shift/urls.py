from django.urls import path

from shift.api import AvailableShift, AssignShift, WorkShiftAPI, BarberShifts

urlpatterns = [
    path('barber/<int:barber_id>/available/', AvailableShift.as_view()),
    path('barber/<int:barber_id>/', BarberShifts.as_view()),
    path('assign-shift/', AssignShift.as_view()),
    path('work-shift/', WorkShiftAPI.as_view()),
]