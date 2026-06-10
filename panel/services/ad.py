from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

from shop.models import Ad


MAX_AD_IMAGE_SIZE = (1920, 1080)
AD_IMAGE_QUALITY = 82


def optimize_ad_image(uploaded_image):
    """Resize and convert an uploaded ad image to an optimized WebP file."""
    try:
        uploaded_image.seek(0)

        with Image.open(uploaded_image) as source:
            image = ImageOps.exif_transpose(source)
            image.load()

            has_transparency = image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            image = image.convert('RGBA' if has_transparency else 'RGB')
            image.thumbnail(MAX_AD_IMAGE_SIZE, Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(
                output,
                format='WEBP',
                quality=AD_IMAGE_QUALITY,
                method=6,
            )
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError('El archivo seleccionado no es una imagen válida.')

    filename = f'{Path(uploaded_image.name).stem}.webp'
    return ContentFile(output.getvalue(), name=filename)


def get_ads_context(search=''):
    ads = Ad.objects.all().order_by('order')
    if search:
        ads = ads.filter(name__icontains=search)
    return {
        'ads': ads,
        'search': search,
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
    ad = Ad.objects.filter(name=name.strip()).exists()
    if ad:
        raise ValueError('El nombre del anuncio ya existe. Por favor, elige otro nombre.')

    if not name or not name.strip():
        raise ValueError('El nombre del anuncio no puede estar vacío.')
    if len(name.strip()) > 50:
        raise ValueError('El nombre del anuncio no puede superar los 50 caracteres.')
    if not isinstance(order, int) or order < 0:
        raise ValueError('El orden debe ser un número entero igual o mayor que cero.')
    if not image:
        raise ValueError('Debes seleccionar una imagen para el anuncio.')

    optimized_image = optimize_ad_image(image)

    ad = Ad.objects.create(
        name=name.strip(),
        order=order,
        image=optimized_image,
    )
    return ad


def update_ad(ad_id, name, order, image=None):
    """Update an existing ad."""
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        raise ValueError('Anuncio no encontrado.')
    
    ad_with_name = Ad.objects.filter(name=name.strip()).exclude(id=ad_id).exists()
    if ad_with_name:
            raise ValueError('El nombre del anuncio ya existe. Por favor, elige otro nombre.')
    if not name or not name.strip():
        raise ValueError('El nombre del anuncio no puede estar vacío.')
    if len(name.strip()) > 50:
        raise ValueError('El nombre del anuncio no puede superar los 50 caracteres.')
    if not isinstance(order, int) or order < 0:
        raise ValueError('El orden debe ser un número entero igual o mayor que cero.')
    
    ad.name = name.strip()
    ad.order = order
    
    if image:
        old_image_name = ad.image.name
        old_image_storage = ad.image.storage
        ad.image = optimize_ad_image(image)

    ad.save()

    if image and old_image_name and old_image_name != ad.image.name:
        old_image_storage.delete(old_image_name)

    return ad


def delete_ad(ad_id):
    """Delete an ad and its related image file."""
    try:
        ad = Ad.objects.get(id=ad_id)
        image_name = ad.image.name
        image_storage = ad.image.storage

        ad.delete()

        if image_name:
            image_storage.delete(image_name)

        return True
    except Ad.DoesNotExist:
        raise ValueError('Anuncio no encontrado.')
