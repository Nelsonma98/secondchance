from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db.models import Q
from PIL import Image, ImageOps, UnidentifiedImageError

from shop.models import Product, Category, Currency

MAX_PRODUCT_IMAGE_SIZE = (1920, 1080)
PRODUCT_IMAGE_QUALITY = 82


def optimize_product_image(uploaded_image):
    """Resize and convert an uploaded product image to an optimized WebP file."""
    try:
        uploaded_image.seek(0)

        with Image.open(uploaded_image) as source:
            image = ImageOps.exif_transpose(source)
            image.load()

            has_transparency = image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            image = image.convert('RGBA' if has_transparency else 'RGB')
            image.thumbnail(MAX_PRODUCT_IMAGE_SIZE, Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(
                output,
                format='WEBP',
                quality=PRODUCT_IMAGE_QUALITY,
                method=6,
            )
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError('El archivo seleccionado no es una imagen válida.')

    filename = f'{Path(uploaded_image.name).stem}.webp'
    return ContentFile(output.getvalue(), name=filename)


def get_products_context(search=''):
    products = Product.objects.select_related('category', 'currency').order_by('-created_at')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(id__icontains=search)
        )

    return {
        'products': products,
        'categories': Category.objects.all().order_by('name'),
        'currencies': Currency.objects.all().order_by('name'),
        'search': search,
    }


def get_create_product_context():
    categories = Category.objects.all()
    currencies = Currency.objects.all()
    return {
        'categories': categories,
        'currencies': currencies,
    }


def get_edit_product_context(product_id):
    try:
        product = Product.objects.get(id=product_id)
        categories = Category.objects.all()
        currencies = Currency.objects.all()
        return {
            'product': product,
            'categories': categories,
            'currencies': currencies,
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


def create_product(name, description, price, contact_phone, category_id, currency_id, image=None):
    """Create a new product."""
    if not name or not name.strip():
        raise ValueError('Product name cannot be empty')
    product_with_same_name = Product.objects.filter(name=name.strip()).exists()
    if product_with_same_name:
        raise ValueError('El nombre del producto ya existe. Por favor, elige otro nombre.')
    if not price or float(price) <= 0:
        raise ValueError('Price must be greater than 0')
    if not contact_phone or not contact_phone.strip():
        raise ValueError('Contact phone cannot be empty')
    if not image:
        raise ValueError('Debes seleccionar una imagen para el producto.')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValueError('Category not found')

    try:
        currency = Currency.objects.get(id=currency_id)
    except Currency.DoesNotExist:
        raise ValueError('Moneda no encontrada.')
    
    image = optimize_product_image(image)

    product = Product.objects.create(
        name=name.strip(),
        description=description.strip() if description else '',
        price=price,
        contact_phone=contact_phone.strip(),
        category=category,
        currency=currency,
        image=image,
    )
    return product


def update_product(product_id, name, description, price, contact_phone, category_id, currency_id, image=None):
    """Update an existing product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValueError('Product not found')
    
    if not name or not name.strip():
        raise ValueError('Product name cannot be empty')
    product_with_same_name = Product.objects.filter(name=name.strip()).exclude(id=product_id).exists()
    if product_with_same_name:
        raise ValueError('El nombre del producto ya existe. Por favor, elige otro nombre.')
    if not price or float(price) <= 0:
        raise ValueError('Price must be greater than 0')
    if not contact_phone or not contact_phone.strip():
        raise ValueError('Contact phone cannot be empty')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValueError('Category not found')

    try:
        currency = Currency.objects.get(id=currency_id)
    except Currency.DoesNotExist:
        raise ValueError('Moneda no encontrada.')
    
    product.name = name.strip()
    product.description = description.strip() if description else ''
    product.price = price
    product.contact_phone = contact_phone.strip()
    product.category = category
    product.currency = currency
    
    if image:
        old_image_name = product.image.name
        old_image_storage = product.image.storage
        product.image = optimize_product_image(image)

    product.save()

    if image and old_image_name and old_image_name != product.image.name:
        old_image_storage.delete(old_image_name)

    return product


def delete_product(product_id):
    """Delete a product and its related image file."""
    try:
        product = Product.objects.get(id=product_id)
        image_name = product.image.name
        image_storage = product.image.storage

        product.delete()

        if image_name:
            image_storage.delete(image_name)

        return True
    except Product.DoesNotExist:
        raise ValueError('Product not found')
