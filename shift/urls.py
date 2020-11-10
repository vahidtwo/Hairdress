from django.urls import path

from shift.api import AvailableShift

urlpatterns = [
    path('available/', AvailableShift.as_view()),
]