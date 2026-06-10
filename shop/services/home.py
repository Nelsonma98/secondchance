from urllib.parse import urlencode

from django.db.models import Q
from shop.models import Ad, Category, Product
from django.core.paginator import Paginator

def get_ads_context():
    ads = Ad.objects.all().order_by('order')
    return ads

def get_categories_context():
    categories = (
        Category.objects
        .filter(products__isnull=False)
        .distinct()
        .order_by('name')
    )
    return categories

def get_products_context(category_ids, search, page):
    products = Product.objects.select_related('category', 'currency')
    if category_ids:
        products = products.filter(category_id__in=category_ids)
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(id__icontains=search)
        )

    products = products.order_by('-created_at')

    paginator = Paginator(products, 12)

    page_obj = paginator.get_page(page)

    return page_obj

def get_home_context(category_ids, search, page):
    try:
        search = search.strip()
        selected_category_ids = []
        for category_id in category_ids:
            try:
                selected_category_ids.append(int(category_id))
            except (TypeError, ValueError):
                continue

        ads = get_ads_context()
        categories = get_categories_context()
        available_category_ids = set(categories.values_list('id', flat=True))
        selected_category_ids = sorted(
            set(selected_category_ids) & available_category_ids
        )
        for category in categories:
            toggled_ids = set(selected_category_ids)
            if category.id in toggled_ids:
                toggled_ids.remove(category.id)
            else:
                toggled_ids.add(category.id)

            filter_params = [
                ('category_id', category_id) for category_id in sorted(toggled_ids)
            ]
            if search:
                filter_params.append(('search', search))

            query = urlencode(filter_params)
            category.filter_url = f'?{query}' if query else '?'

        products = get_products_context(selected_category_ids, search, page)
        pagination_params = [
            ('category_id', category_id) for category_id in selected_category_ids
        ]
        if search:
            pagination_params.append(('search', search))
        previous_page_url = None
        next_page_url = None

        if products.has_previous():
            previous_page_url = '?' + urlencode(
                pagination_params + [('page', products.previous_page_number())]
            )
        if products.has_next():
            next_page_url = '?' + urlencode(
                pagination_params + [('page', products.next_page_number())]
            )

        return {
            'ads': ads,
            'categories': categories,
            'products': products,
            'search': search,
            'selected_category_ids': selected_category_ids,
            'previous_page_url': previous_page_url,
            'next_page_url': next_page_url,
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
