from core import models


class Service(models.AbstractBaseModel):
    name = models.CharField(max_length=255)
    price_per_15_min = models.IntegerField()

    def __str__(self):
        return f'[{self.id}] {self.name}'