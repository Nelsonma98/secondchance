from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from panel.services.ad import (
    get_ads_context,
    create_ad as service_create_ad,
    update_ad,
    delete_ad as service_delete_ad,
)


@login_required
def ads_panel(request):
    search = request.GET.get('search', '').strip()
    context = get_ads_context(search)
    return render(request, 'ad/ads-panel.html', context)


@login_required
def create_ad(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            order = int(request.POST.get('order', 0))
            image = request.FILES.get('image')
            
            service_create_ad(name, order, image)
            messages.success(request, 'Anuncio creado correctamente.')
            return redirect('ads_panel')
        except (ValueError, TypeError) as e:
            messages.error(request, str(e))

    return redirect('ads_panel')


@login_required
def edit_ad(request, ad_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            order = int(request.POST.get('order', 0))
            image = request.FILES.get('image')
            
            update_ad(ad_id, name, order, image)
            messages.success(request, 'Anuncio actualizado correctamente.')
            return redirect('ads_panel')
        except (ValueError, TypeError) as e:
            messages.error(request, str(e))

    return redirect('ads_panel')


@login_required
def delete_ad(request, ad_id):
    if request.method == 'POST':
        try:
            service_delete_ad(ad_id)
            messages.success(request, 'Anuncio eliminado correctamente.')
            return redirect('ads_panel')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('ads_panel')
