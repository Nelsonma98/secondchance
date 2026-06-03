from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from panel.services.ad import (
    get_ads_context,
    get_create_ad_context,
    get_edit_ad_context,
    get_delete_ad_context,
    create_ad as service_create_ad,
    update_ad,
    delete_ad as service_delete_ad,
)


@login_required
def ads_panel(request):
    context = get_ads_context()
    return render(request, 'ad/ads-panel.html', context)


@login_required
def create_ad(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            order = int(request.POST.get('order', 0))
            image = request.FILES.get('image')
            
            service_create_ad(name, order, image)
            return redirect('ads_panel')
        except (ValueError, TypeError) as e:
            return render(request, 'ad/create-ad.html', {
                'error': str(e),
                'form_data': request.POST
            })
    
    context = get_create_ad_context()
    return render(request, 'ad/create-ad.html', context)


@login_required
def edit_ad(request, ad_id):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            order = int(request.POST.get('order', 0))
            image = request.FILES.get('image')
            
            update_ad(ad_id, name, order, image)
            return redirect('ads_panel')
        except (ValueError, TypeError) as e:
            context = get_edit_ad_context(ad_id)
            context['error'] = str(e)
            context['form_data'] = request.POST
            return render(request, 'ad/edit-ad.html', context)
    
    context = get_edit_ad_context(ad_id)
    return render(request, 'ad/edit-ad.html', context)


@login_required
def delete_ad(request, ad_id):
    if request.method == 'POST':
        try:
            service_delete_ad(ad_id)
            return redirect('ads_panel')
        except ValueError as e:
            context = get_delete_ad_context(ad_id)
            context['error'] = str(e)
            return render(request, 'ad/delete-ad.html', context)
    
    context = get_delete_ad_context(ad_id)
    return render(request, 'ad/delete-ad.html', context)
