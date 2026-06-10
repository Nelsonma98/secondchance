from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from panel.services.currency import (
    get_currencies_context,
    create_currency as service_create_currency,
    update_currency,
    delete_currency as service_delete_currency,
)


@login_required
def currencies_panel(request):
    search = request.GET.get('search', '').strip()
    context = get_currencies_context(search)
    return render(request, 'currency/currencies-panel.html', context)


@login_required
def create_currency(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            service_create_currency(name)
            messages.success(request, 'currencía creada correctamente.')
            return redirect('currencies_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('currencies_panel')


@login_required
def edit_currency(request, currency_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            update_currency(currency_id, name)
            messages.success(request, 'currencía actualizada correctamente.')
            return redirect('currencies_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('currencies_panel')


@login_required
def delete_currency(request, currency_id):
    if request.method == 'POST':
        try:
            service_delete_currency(currency_id)
            messages.success(request, 'currencía eliminada correctamente.')
            return redirect('currencies_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('currencies_panel')
