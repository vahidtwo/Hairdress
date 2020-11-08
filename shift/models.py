from django.db.models import Q

from core import models


class Shift(models.AbstractBaseModel):
    customer = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='shifts')
    barber = models.ForeignKey('barber.Barber', on_delete=models.PROTECT, related_name='shifts')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    price = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    def available(self):
        return Shift.objects.filter(Q(barber=self.barber) | Q(customer=self.customer)).filter(
            models.Q(start_at__lte=self.start_at, end_at__gte=self.end_at) |
            models.Q(start_at__lte=self.start_at, end_at__lte=self.end_at, end_at__gt=self.start_at) |
            models.Q(start_at__gte=self.start_at, end_at__gte=self.end_at, start_at__lt=self.end_at) |
            models.Q(start_at__gte=self.start_at, end_at__lte=self.end_at)).exists()

    def save(self, *args, **kwargs):
        if self.available():
            return super().save(*args, **kwargs)
        raise ValueError('نوبت تداخل دارد')
