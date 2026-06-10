from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from panel.services.product import (
    get_products_context,
    create_product as service_create_product,
    update_product,
    delete_product as service_delete_product,
)


@login_required
def products_panel(request):
    search = request.GET.get('search', '').strip()
    context = get_products_context(search)
    return render(request, 'product/products-panel.html', context)


@login_required
def create_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '')
            contact_phone = request.POST.get('contact_phone', '').strip()
            category_id = request.POST.get('category_id', '')
            currency_id = request.POST.get('currency_id', '')
            image = request.FILES.get('image')
            
            service_create_product(
                name, description, price, contact_phone,
                category_id, currency_id, image
            )
            messages.success(request, 'Producto creado correctamente.')
            return redirect('products_panel')
        except (ValueError, TypeError) as e:
            messages.error(request, str(e))

    return redirect('products_panel')


@login_required
def edit_product(request, product_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '')
            contact_phone = request.POST.get('contact_phone', '').strip()
            category_id = request.POST.get('category_id', '')
            currency_id = request.POST.get('currency_id', '')
            image = request.FILES.get('image')
            
            update_product(
                product_id, name, description, price, contact_phone,
                category_id, currency_id, image
            )
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('products_panel')
        except (ValueError, TypeError) as e:
            messages.error(request, str(e))

    return redirect('products_panel')


@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            service_delete_product(product_id)
            messages.success(request, 'Producto eliminado correctamente.')
            return redirect('products_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('products_panel')
