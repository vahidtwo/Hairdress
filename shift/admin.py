from django.contrib import admin

# Register your models here.
from shift.models import WorkShift, Shift

admin.site.register(WorkShift)
admin.site.register(Shift)
