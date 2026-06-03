from shop.models import Ad, Category, Product
from django.core.paginator import Paginator

def get_ads_context():
    ads = Ad.objects.all().order_by('order')
    return ads

def get_categories_context():
    categories = Category.objects.all().order_by('-created_at')
    return categories

def get_products_context(category_id, page):
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)

    products = products.order_by('-created_at')

    paginator = Paginator(products, 12)

    page_obj = paginator.get_page(page)

    return page_obj

def get_home_context(category_id, page):
    try:
        ads = get_ads_context()
        categories = get_categories_context()
        products = get_products_context(category_id, page)

        return {
            'ads': ads,
            'categories': categories,
            'products': products,
        }
    except:
        return {'error': 'Ha ocurrido un error inesperado.'}
    
def get_product_context(product_id):
    try:
        product = Product.objects.get(id=product_id)

        return {
            'product': product, 
        }
    except Product.DoesNotExist:
        return {'error': 'Producto no encontrado'}