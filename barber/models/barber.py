from core import models


class Barber(models.AbstractBaseModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='barber')
    services = models.ManyToManyField('barber.service', related_name='barber')

    def __str__(self):
        return f'[{self.id}] {self.user.username}'