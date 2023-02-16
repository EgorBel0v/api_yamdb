import re
from django.core.exceptions import ValidationError


def ValidationUsername(value):
    """"Валидация для Юзернейма."""
    
    if value == 'me':
        raise ValidationError(
            ('<me> не может быть именем пользователя, придумайте другое имя.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Недопустимые символы <{value}> в нике.'),
            params={'value': value},
        )