from django.core.exceptions import ValidationError

def alphabet(value):

    alpha = r'^[a-zA-Z]*$'

    if alpha in value:
        return value
    else:
        raise ValidationError('Only alphabet characters are allowed.')

