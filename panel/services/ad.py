from shop.models import Ad


def get_ads_context():
    ads = Ad.objects.all().order_by('order')
    return {
        'ads': ads,
    }


def get_create_ad_context():
    return {}


def get_edit_ad_context(ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
        return {
            'ad': ad,
        }
    except Ad.DoesNotExist:
        return {'error': 'Ad not found'}


def get_delete_ad_context(ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
        return {
            'ad': ad,
        }
    except Ad.DoesNotExist:
        return {'error': 'Ad not found'}


def create_ad(name, order, image=None):
    """Create a new ad."""
    if not name or not name.strip():
        raise ValueError('Ad name cannot be empty')
    if not isinstance(order, int) or order < 0:
        raise ValueError('Order must be a non-negative integer')
    
    ad = Ad.objects.create(
        name=name.strip(),
        order=order,
        image=image,
    )
    return ad


def update_ad(ad_id, name, order, image=None):
    """Update an existing ad."""
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        raise ValueError('Ad not found')
    
    if not name or not name.strip():
        raise ValueError('Ad name cannot be empty')
    if not isinstance(order, int) or order < 0:
        raise ValueError('Order must be a non-negative integer')
    
    ad.name = name.strip()
    ad.order = order
    
    if image:
        ad.image = image
    
    ad.save()
    return ad


def delete_ad(ad_id):
    """Delete an ad."""
    try:
        ad = Ad.objects.get(id=ad_id)
        ad.delete()
        return True
    except Ad.DoesNotExist:
        raise ValueError('Ad not found')
