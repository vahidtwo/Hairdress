from django.urls import path

from barber.api import CRUDBarber, CRUDService

urlpatterns = [
    path('<int:barber_id>/', CRUDBarber.as_view()),
    path('', CRUDBarber.as_view()),
    path('service/<int:barber_id>/', CRUDService.as_view()),
    path('service/', CRUDService.as_view()),
]
