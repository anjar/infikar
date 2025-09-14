from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .username_rules import is_reserved_username, is_valid_username_length, MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH


def validate_username(value):
    """
    Validate username format.
    Username can only contain letters, numbers, dots, hyphens, and underscores.
    """
    if not value:
        raise ValidationError(
            _('Username is required.'),
            code='required_username'
        )
    
    # Check length
    if not is_valid_username_length(value):
        raise ValidationError(
            _(f'Username must be {MIN_USERNAME_LENGTH}-{MAX_USERNAME_LENGTH} characters long.'),
            code='invalid_length'
        )
    
    if not re.match(r'^[a-zA-Z0-9._-]+$', value):
        raise ValidationError(
            _('Username can only contain letters, numbers, dots, hyphens, and underscores.'),
            code='invalid_username'
        )
    
    # Check for consecutive dots or hyphens
    if '..' in value or '--' in value or '.-' in value or '-.' in value:
        raise ValidationError(
            _('Username cannot contain consecutive dots or hyphens.'),
            code='invalid_username'
        )
    
    # Check for starting/ending with dots or hyphens
    if value.startswith(('.', '-')) or value.endswith(('.', '-')):
        raise ValidationError(
            _('Username cannot start or end with a dot or hyphen.'),
            code='invalid_username'
        )
    
    # Check for reserved usernames
    if is_reserved_username(value):
        raise ValidationError(
            _('This username is reserved and cannot be used.'),
            code='reserved_username'
        )


# Custom username validators for allauth
custom_username_validators = [validate_username]
