from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class MobileNumberValidator(validators.RegexValidator):
    regex = r'^[0][9]\d{9}$'
    message = 'Enter a valid mobile number, start with 09 and followed by 8, 13 digits.'
    flags = 0
