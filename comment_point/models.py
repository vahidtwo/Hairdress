from core import model


class Comment(model.AbstractBaseModel):
    body = model.TextField()
    title = model.CharField(max_length=255)
    shift = model.OneToOneField('shift.Shift', related_name='comment', on_delete=model.PROTECT)
    user = model.ForeignKey('accounts.User', related_name='comments', on_delete=model.CASCADE)

    def save(self, *args, **kwargs):
        if self.user == self.shift.customer:
            return super().save(*args, **kwargs)
        raise ValueError('نظر دهنده با مشتری یکسان نیست')


class Point(model.AbstractBaseModel):
    point = model.IntegerField(choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    shift = model.OneToOneField('shift.Shift', related_name='point', on_delete=model.PROTECT)
    user = model.ForeignKey('accounts.User', related_name='point', on_delete=model.CASCADE)
