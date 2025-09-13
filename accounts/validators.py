from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_username(value):
    """
    Validate username format.
    Username can only contain letters, numbers, dots, hyphens, and underscores.
    """
    if not re.match(r'^[a-zA-Z0-9._-]+$', value):
        raise ValidationError(
            _('Username can only contain letters, numbers, dots, hyphens, and underscores.'),
            code='invalid_username'
        )
    
    # Check for consecutive dots
    if '..' in value:
        raise ValidationError(
            _('Username cannot contain consecutive dots.'),
            code='invalid_username'
        )
    
    # Check for starting/ending with dots
    if value.startswith('.') or value.endswith('.'):
        raise ValidationError(
            _('Username cannot start or end with a dot.'),
            code='invalid_username'
        )
    
    # Check for reserved usernames
    reserved_usernames = [
        'admin', 'administrator', 'api', 'app', 'www', 'mail', 'ftp', 'root',
        'support', 'help', 'contact', 'about', 'terms', 'privacy', 'login',
        'register', 'signup', 'signin', 'logout', 'dashboard', 'profile',
        'settings', 'account', 'user', 'users', 'blog', 'news', 'home',
        'index', 'main', 'default', 'test', 'demo', 'example', 'sample'
    ]
    
    if value.lower() in reserved_usernames:
        raise ValidationError(
            _('This username is reserved and cannot be used.'),
            code='reserved_username'
        )


# Custom username validators for allauth
custom_username_validators = [validate_username]
