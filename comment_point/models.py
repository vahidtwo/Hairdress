from core import models


class Comment(models.AbstractBaseModel):
    body = models.TextField()
    title = models.CharField(max_length=255)
    shift = models.OneToOneField('shift.Shift', related_name='comment', on_delete=models.PROTECT)
    user = models.ForeignKey('accounts.User', related_name='comments', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.user == self.shift.customer:
            return super().save(*args, **kwargs)
        raise ValueError('نظر دهنده با مشتری یکسان نیست')


class Point(models.AbstractBaseModel):
    point = models.IntegerField(choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    shift = models.OneToOneField('shift.Shift', related_name='point', on_delete=models.PROTECT)
    user = models.ForeignKey('accounts.User', related_name='point', on_delete=models.CASCADE)
