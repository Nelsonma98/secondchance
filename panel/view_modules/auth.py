from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from panel.services.auth import build_login_context


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', build_login_context())

    user = authenticate(
        request,
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )

    if user is None:
        return render(request, 'login.html', build_login_context(error='Usuario o contraseña incorrecta.'))

    auth_login(request, user)
    return redirect('/panel/products')

def logout(request):
    auth_logout(request)
    return redirect('/panel/login/')