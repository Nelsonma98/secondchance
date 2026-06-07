from django.contrib import messages
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from panel.services.dashboard import (
    create_user as service_create_user,
    delete_current_user,
    get_panel_context,
    update_current_password,
    update_current_username,
)


@login_required
def panel(request):
    return render(request, 'panel.html', get_panel_context(request.user))


@login_required
@require_POST
def update_profile_username(request):
    try:
        update_current_username(request.user, request.POST.get('username', ''))
        messages.success(request, 'Nombre de usuario actualizado correctamente.')
    except ValueError as error:
        messages.error(request, str(error))

    return redirect('panel')


@login_required
@require_POST
def update_profile_password(request):
    try:
        user = update_current_password(
            request.user,
            request.POST.get('current_password', ''),
            request.POST.get('new_password', ''),
            request.POST.get('confirm_password', ''),
        )
        update_session_auth_hash(request, user)
        messages.success(request, 'Contraseña actualizada correctamente.')
    except ValueError as error:
        messages.error(request, str(error))

    return redirect('panel')


@login_required
@require_POST
def delete_profile(request):
    try:
        username = delete_current_user(
            request.user,
            request.POST.get('current_password', ''),
        )
    except ValueError as error:
        messages.error(request, str(error))
        return redirect('panel')

    auth_logout(request)
    messages.success(request, f'La cuenta “{username}” fue eliminada correctamente.')
    return redirect('login')


@login_required
@require_POST
def create_user(request):
    try:
        user = service_create_user(
            request.POST.get('username', ''),
            request.POST.get('password', ''),
            request.POST.get('confirm_password', ''),
        )
        messages.success(request, f'Usuario “{user.username}” creado correctamente.')
    except ValueError as error:
        messages.error(request, str(error))

    return redirect('panel')
