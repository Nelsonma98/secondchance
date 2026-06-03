from shop.models import Product, Category


def get_products_context():
    products = Product.objects.all().order_by('-created_at')
    return {
        'products': products,
    }


def get_create_product_context():
    categories = Category.objects.all()
    return {
        'categories': categories,
    }


def get_edit_product_context(product_id):
    try:
        product = Product.objects.get(id=product_id)
        categories = Category.objects.all()
        return {
            'product': product,
            'categories': categories,
        }
    except Product.DoesNotExist:
        return {'error': 'Product not found'}


def get_delete_product_context(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return {
            'product': product,
        }
    except Product.DoesNotExist:
        return {'error': 'Product not found'}


def create_product(name, description, price, contact_phone, category_id, image=None):
    """Create a new product."""
    if not name or not name.strip():
        raise ValueError('Product name cannot be empty')
    if not price or float(price) <= 0:
        raise ValueError('Price must be greater than 0')
    if not contact_phone or not contact_phone.strip():
        raise ValueError('Contact phone cannot be empty')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValueError('Category not found')
    
    product = Product.objects.create(
        name=name.strip(),
        description=description.strip() if description else '',
        price=price,
        contact_phone=contact_phone.strip(),
        category=category,
        image=image,
    )
    return product


def update_product(product_id, name, description, price, contact_phone, category_id, image=None):
    """Update an existing product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValueError('Product not found')
    
    if not name or not name.strip():
        raise ValueError('Product name cannot be empty')
    if not price or float(price) <= 0:
        raise ValueError('Price must be greater than 0')
    if not contact_phone or not contact_phone.strip():
        raise ValueError('Contact phone cannot be empty')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValueError('Category not found')
    
    product.name = name.strip()
    product.description = description.strip() if description else ''
    product.price = price
    product.contact_phone = contact_phone.strip()
    product.category = category
    
    if image:
        product.image = image
    
    product.save()
    return product


def delete_product(product_id):
    """Delete a product."""
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return True
    except Product.DoesNotExist:
        raise ValueError('Product not found')
