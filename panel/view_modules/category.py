from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from panel.services.category import (
    get_categories_context,
    get_create_category_context,
    get_edit_category_context,
    get_delete_category_context,
    create_category as service_create_category,
    update_category,
    delete_category as service_delete_category,
)


@login_required
def categories_panel(request):
    context = get_categories_context()
    return render(request, 'category/categories-panel.html', context)


@login_required
def create_category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            service_create_category(name)
            return redirect('categories_panel')
        except ValueError as e:
            return render(request, 'category/create-category.html', {
                'error': str(e),
                'name': request.POST.get('name', '')
            })
    
    context = get_create_category_context()
    return render(request, 'category/create-category.html', context)


@login_required
def edit_category(request, category_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            update_category(category_id, name)
            return redirect('categories_panel')
        except ValueError as e:
            context = get_edit_category_context(category_id)
            context['error'] = str(e)
            return render(request, 'category/edit-category.html', context)
    
    context = get_edit_category_context(category_id)
    return render(request, 'category/edit-category.html', context)


@login_required
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            service_delete_category(category_id)
            return redirect('categories_panel')
        except ValueError as e:
            context = get_delete_category_context(category_id)
            context['error'] = str(e)
            return render(request, 'category/delete-category.html', context)
    
    context = get_delete_category_context(category_id)
    return render(request, 'category/delete-category.html', context)
