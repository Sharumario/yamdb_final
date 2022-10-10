import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            f'{value} явлеятся некорректным username!')
    incorrect_symbols = re.findall(r'[^\w[.@+-]+', value)
    if incorrect_symbols:
        raise ValidationError(
            f'Недопустимые символы в username: {incorrect_symbols}'
        )
    return value


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
    return value
