from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user is None:
            return render(request,'login.html', {
                'form': AuthenticationForm,
                'error': 'Invalid username or password'
            })
        else:
            auth_login(request, user)
            return redirect('panel')


def panel(request):
    return render(request, 'panel.html')

def category_panel(request):
    return render(request,'category-panel.html')

def product_panel(request):
    return render(request,'product-panel.html')

def ad_panel(request):
    return render(request,'ad-panel.html')