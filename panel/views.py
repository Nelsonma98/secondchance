from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
# AUTHENTICATION
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

# PANEL
@login_required
def panel(request):
    return render(request, 'panel.html')

# Category
@login_required
def categories_panel(request):
    return render(request,'category/categories-panel.html')

@login_required
def create_category(request):
    return render(request,'category/create-category.html')

@login_required
def edit_category(request, category_id):
    return render(request,'category/edit-category.html',{
        'id': category_id
    })

@login_required
def delete_category(request, category_id):
    return render(request,'category/delete-category.html')

# Product
@login_required
def products_panel(request):
    return render(request,'product/products-panel.html')

@login_required
def create_product(request):
    return render(request,'product/create-product.html')

@login_required
def edit_product(request, product_id):
    return render(request,'product/edit-product.html')

@login_required
def delete_product(request, product_id):
    return render(request,'product/delete-product.html')

# Ad
@login_required
def ads_panel(request):
    return render(request,'ad/ads-panel.html')

@login_required
def create_ad(request):
    return render(request,'ad/create-ad.html')

@login_required
def edit_ad(request, ad_id):
    return render(request,'ad/edit-ad.html')

@login_required
def delete_ad(request, ad_id):
    return render(request,'ad/delete-ad.html')