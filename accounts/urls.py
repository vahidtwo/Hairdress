from django.urls import path

from accounts.api import LogOut, CRUDCustomer, LoginAPI, ChangePassword

urlpatterns = [
    path('log-out/', LogOut.as_view()),
    path('', CRUDCustomer.as_view()),
    path('<int:user_id>/', CRUDCustomer.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('login/', LoginAPI.as_view()),
]
