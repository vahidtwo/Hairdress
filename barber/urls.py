from django.urls import path

from barber.api import CRUDBarber, CRUDService, AssignService

urlpatterns = [
    path('<int:barber_id>/', CRUDBarber.as_view()),
    path('', CRUDBarber.as_view()),
    path('service/<int:service_id>/', CRUDService.as_view()),
    path('service/', CRUDService.as_view()),
    path('assign-service/', AssignService.as_view()),
]
