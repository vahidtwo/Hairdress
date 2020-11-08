from core import model


class Service(model.AbstractBaseModel):
    name = model.CharField(max_length=255)
    price_per_15_min = model.IntegerField()