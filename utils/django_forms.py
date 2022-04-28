import re

from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val
    
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError(
            (
                'Senha é fraca. '
                'Sua senha deve conter: '
                'Pelo menos uma letra minuscula e um numero '
                '8 caracteres'
            ),
            code='invalid'
        )
