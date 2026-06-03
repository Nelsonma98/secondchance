from shop.models import Category


def get_categories_context():
    categories = Category.objects.all().order_by('-created_at')
    return {
        'categories': categories,
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
        return {'error': 'Category not found'}


def get_delete_category_context(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return {
            'category': category,
        }
    except Category.DoesNotExist:
        return {'error': 'Category not found'}


def create_category(name):
    """Create a new category."""
    if not name or not name.strip():
        raise ValueError('Category name cannot be empty')
    
    category = Category.objects.create(name=name.strip())
    return category


def update_category(category_id, name):
    """Update an existing category."""
    try:
        category = Category.objects.get(id=category_id)
        if not name or not name.strip():
            raise ValueError('Category name cannot be empty')
        
        category.name = name.strip()
        category.save()
        return category
    except Category.DoesNotExist:
        raise ValueError('Category not found')


def delete_category(category_id):
    """Delete a category."""
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return True
    except Category.DoesNotExist:
        raise ValueError('Category not found')
