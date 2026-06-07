from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from panel.services.category import (
    get_categories_context,
    create_category as service_create_category,
    update_category,
    delete_category as service_delete_category,
)


@login_required
def categories_panel(request):
    search = request.GET.get('search', '').strip()
    context = get_categories_context(search)
    return render(request, 'category/categories-panel.html', context)


@login_required
def create_category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            service_create_category(name)
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('categories_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('categories_panel')


@login_required
def edit_category(request, category_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            update_category(category_id, name)
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('categories_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('categories_panel')


@login_required
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            service_delete_category(category_id)
            messages.success(request, 'Categoría eliminada correctamente.')
            return redirect('categories_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('categories_panel')
