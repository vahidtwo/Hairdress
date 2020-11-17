import jdatetime
from django.db.models import Q

from barber.models import Barber
from core import models


class Shift(models.AbstractBaseModel):
    customer = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='shifts')
    barber = models.ForeignKey('barber.Barber', on_delete=models.PROTECT, related_name='shifts')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    price = models.IntegerField(editable=False)
    service = models.ForeignKey('barber.Service', on_delete=models.SET_NULL, null=True, blank=True)

    def available(self):
        return not Shift.objects.filter(Q(barber=self.barber) | Q(customer=self.customer)).filter(
            models.Q(start_at__lte=self.start_at, end_at__gte=self.end_at) |
            models.Q(start_at__lte=self.start_at, end_at__lte=self.end_at, end_at__gt=self.start_at) |
            models.Q(start_at__gte=self.start_at, end_at__gte=self.end_at, start_at__lt=self.end_at) |
            models.Q(start_at__gte=self.start_at, end_at__lte=self.end_at)).exists()

    def is_in_work_shift(self):
        work_shift = WorkShift.objects.first()
        usual_day_start_morning = work_shift.usual_day_start_morning
        usual_day_start_morning = jdatetime.time(hour=usual_day_start_morning.hour,
                                                 minute=usual_day_start_morning.minute)
        usual_day_start_afternoon = work_shift.usual_day_start_afternoon
        usual_day_start_afternoon = jdatetime.time(hour=usual_day_start_afternoon.hour,
                                                   minute=usual_day_start_afternoon.minute)
        usual_day_end_morning = work_shift.usual_day_end_morning
        usual_day_end_morning = jdatetime.time(hour=usual_day_end_morning.hour, minute=usual_day_end_morning.minute)
        usual_day_end_afternoon = work_shift.usual_day_end_afternoon
        usual_day_end_afternoon = jdatetime.time(hour=usual_day_end_afternoon.hour,
                                                 minute=usual_day_end_afternoon.minute)
        if (usual_day_start_morning <= self.start_at.time() < usual_day_end_morning) or \
                (usual_day_start_afternoon <= self.start_at.time() < usual_day_end_afternoon):
            return True
        return False

    def save(self, *args, **kwargs):
        if self.service not in self.barber.services.all():
            raise ValueError('این ارایشگر این سرویس را ارایه نمیدهد')
        self.end_at = self.end_at.replace(second=0)
        self.start_at = self.start_at.replace(second=0)
        delta = (self.end_at - self.start_at).seconds // 60
        if delta not in [15, 30, 45, 0]:
            raise ValueError('نوبت باید در بازه  ۱۵ ۳۰ ۴۵ 60 دقیقه باشد')
        self.price = int(delta // 15 * self.service.price_per_15_min)
        if self.start_at >= self.end_at:
            raise ValueError('start_at >= end_at')
        if delta < 5:
            raise ValueError('نوبت کمتر از 5 دقیقه است')
        if not self.is_in_work_shift():
            raise ValueError('تایم در شیفت کاری نمی باشد')
        if self.available():
            return super().save(*args, **kwargs)
        raise ValueError('نوبت تداخل دارد')


class WorkShift(models.AbstractBaseModel):
    usual_day_start_morning = models.TimeField()
    usual_day_end_morning = models.TimeField()
    usual_day_start_afternoon = models.TimeField()
    usual_day_end_afternoon = models.TimeField()
