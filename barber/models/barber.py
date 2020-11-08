from core import model


class Barber(model.AbstractBaseModel):
    user = model.OneToOneField('accounts.User', on_delete=model.CASCADE, related_name='barber')
    services = model.ManyToManyField('barber.service', related_name='barber')