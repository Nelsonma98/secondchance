from django.shortcuts import render, redirect

from shop.services.home import (
    get_home_context,
    get_product_context,
)

def home(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        page = request.GET.get('page', 1)

        res = get_home_context(category_id, page)

        return render(request, 'home.html', res)
    
def product(request, product_id):
    if request.method == 'GET':
        try:
            product = get_product_context(product_id)

            return render(request, 'product.html', product_id)
        except Exception as e:
            return render(request, 'product.html', {
                'error': str(e)
            })