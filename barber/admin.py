from django.contrib import admin

# Register your models here.
from barber.models import Barber, Service

admin.site.register(Barber)
admin.site.register(Service)
