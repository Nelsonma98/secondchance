from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from panel.services.product import (
    get_products_context,
    get_create_product_context,
    get_edit_product_context,
    get_delete_product_context,
    create_product as service_create_product,
    update_product,
    delete_product as service_delete_product,
)


@login_required
def products_panel(request):
    context = get_products_context()
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
            image = request.FILES.get('image')
            
            service_create_product(name, description, price, contact_phone, category_id, image)
            return redirect('products_panel')
        except ValueError as e:
            context = get_create_product_context()
            context['error'] = str(e)
            context['form_data'] = request.POST
            return render(request, 'product/create-product.html', context)
    
    context = get_create_product_context()
    return render(request, 'product/create-product.html', context)


@login_required
def edit_product(request, product_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '')
            contact_phone = request.POST.get('contact_phone', '').strip()
            category_id = request.POST.get('category_id', '')
            image = request.FILES.get('image')
            
            update_product(product_id, name, description, price, contact_phone, category_id, image)
            return redirect('products_panel')
        except ValueError as e:
            context = get_edit_product_context(product_id)
            context['error'] = str(e)
            context['form_data'] = request.POST
            return render(request, 'product/edit-product.html', context)
    
    context = get_edit_product_context(product_id)
    return render(request, 'product/edit-product.html', context)


@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            service_delete_product(product_id)
            return redirect('products_panel')
        except ValueError as e:
            context = get_delete_product_context(product_id)
            context['error'] = str(e)
            return render(request, 'product/delete-product.html', context)
    
    context = get_delete_product_context(product_id)
    return render(request, 'product/delete-product.html', context)
