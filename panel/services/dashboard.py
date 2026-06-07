import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError


User = get_user_model()
USERNAME_PATTERN = re.compile(r'^[\w.@+-]+$')
PASSWORD_ERROR_MESSAGES = {
    'password_too_short': 'La contraseña debe tener al menos 8 caracteres.',
    'password_too_common': 'La contraseña es demasiado común.',
    'password_entirely_numeric': 'La contraseña no puede contener solamente números.',
    'password_too_similar': 'La contraseña se parece demasiado al nombre de usuario.',
}


def get_panel_context(current_user):
    return {
        'users': User.objects.all().order_by('username'),
        'current_user': current_user,
    }


def validate_username(username, current_user=None):
    username = username.strip()

    if not username:
        raise ValueError('El nombre de usuario no puede estar vacío.')
    if len(username) > User._meta.get_field('username').max_length:
        raise ValueError('El nombre de usuario es demasiado largo.')
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            'El nombre de usuario solo puede contener letras, números y los caracteres @, ., +, - y _.'
        )

    matches = User.objects.filter(username__iexact=username)
    if current_user is not None:
        matches = matches.exclude(pk=current_user.pk)
    if matches.exists():
        raise ValueError('Ese nombre de usuario ya está en uso.')

    return username


def validate_new_password(password, confirmation, user):
    if not password:
        raise ValueError('La nueva contraseña no puede estar vacía.')
    if password != confirmation:
        raise ValueError('Las contraseñas no coinciden.')

    try:
        validate_password(password, user=user)
    except ValidationError as error:
        messages = [
            PASSWORD_ERROR_MESSAGES.get(item.code, item.message)
            for item in error.error_list
        ]
        raise ValueError(' '.join(messages))


def update_current_username(user, username):
    user.username = validate_username(username, current_user=user)
    try:
        user.save(update_fields=['username'])
    except IntegrityError:
        raise ValueError('Ese nombre de usuario ya está en uso.')
    return user


def update_current_password(user, current_password, new_password, confirmation):
    if not user.check_password(current_password):
        raise ValueError('La contraseña actual es incorrecta.')

    validate_new_password(new_password, confirmation, user)
    user.set_password(new_password)
    user.save(update_fields=['password'])
    return user


def delete_current_user(user, current_password):
    if not user.check_password(current_password):
        raise ValueError('La contraseña actual es incorrecta.')

    username = user.username
    user.delete()
    return username


def create_user(username, password, confirmation):
    username = validate_username(username)
    candidate = User(username=username)
    validate_new_password(password, confirmation, candidate)
    try:
        return User.objects.create_user(username=username, password=password)
    except IntegrityError:
        raise ValueError('Ese nombre de usuario ya está en uso.')
