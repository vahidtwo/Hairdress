from django.db.models import Q

from core import model


class Shift(model.AbstractBaseModel):
    customer = model.ForeignKey('accounts.User', on_delete=model.PROTECT, related_name='shifts')
    barber = model.ForeignKey('barber.Barber', on_delete=model.PROTECT, related_name='shifts')
    start_at = model.DateTimeField()
    end_at = model.DateTimeField()
    price = model.DecimalField(max_digits=15, decimal_places=2, editable=False)

    def available(self):
        return Shift.objects.filter(Q(barber=self.barber) | Q(customer=self.customer)).filter(
            model.Q(start_at__lte=self.start_at, end_at__gte=self.end_at) |
            model.Q(start_at__lte=self.start_at, end_at__lte=self.end_at, end_at__gt=self.start_at) |
            model.Q(start_at__gte=self.start_at, end_at__gte=self.end_at, start_at__lt=self.end_at) |
            model.Q(start_at__gte=self.start_at, end_at__lte=self.end_at)).exists()

    def save(self, *args, **kwargs):
        if self.available():
            return super().save(*args, **kwargs)
        raise ValueError('نوبت تداخل دارد')
