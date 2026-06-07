from shop.models import Category
from django.db.models import Q


def get_categories_context(search):
    categories = Category.objects.all().order_by('-created_at')
    if search:
        categories = categories.filter(
            Q(name__icontains=search)|
            Q(id__icontains=search)
        )
    return {
        'categories': categories,
        'search': search,
    }


def get_create_category_context():
    return {}


def get_edit_category_context(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return {
            'category': category,
        }
    except Category.DoesNotExist:
        return {'error': 'Categoría no encontrada.'}


def get_delete_category_context(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return {
            'category': category,
        }
    except Category.DoesNotExist:
        return {'error': 'Categoría no encontrada.'}


def create_category(name):
    """Create a new category."""
    category = Category.objects.filter(name=name.strip()).exists()
    if category:
        raise ValueError('El nombre de la categoría ya existe. Por favor, elige otro nombre.')
    if not name or not name.strip():
        raise ValueError('El nombre de la categoría no puede estar vacío.')
    
    category = Category.objects.create(name=name.strip())
    return category


def update_category(category_id, name):
    """Update an existing category."""
    try:
        category = Category.objects.get(id=category_id)
        if not name or not name.strip():
            raise ValueError('El nombre de la categoría no puede estar vacío.')
        
        category_with_name = Category.objects.filter(name=name.strip()).exclude(id=category_id).exists()
        if category_with_name:
            raise ValueError('El nombre de la categoría ya existe. Por favor, elige otro nombre.')
        
        category.name = name.strip()
        category.save()
        return category
    except Category.DoesNotExist:
        raise ValueError('Categoría no encontrada.')


def delete_category(category_id):
    """Delete a category."""
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return True
    except Category.DoesNotExist:
        raise ValueError('Categoría no encontrada.')
