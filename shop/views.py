from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def product(request, product_id):
    return render(request, 'product.html', {
        'id': product_id
    })