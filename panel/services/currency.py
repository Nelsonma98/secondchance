from shop.models import Currency
from django.db.models import Q


def get_currencies_context(search):
    currencies = Currency.objects.all().order_by('-created_at')
    if search:
        currencies = currencies.filter(
            Q(name__icontains=search)|
            Q(id__icontains=search)
        )
    return {
        'currencies': currencies,
        'search': search,
    }


def get_create_currency_context():
    return {}


def get_edit_currency_context(currency_id):
    try:
        currency = Currency.objects.get(id=currency_id)
        return {
            'currency': currency,
        }
    except Currency.DoesNotExist:
        return {'error': 'Moneda no encontrada.'}


def get_delete_currency_context(currency_id):
    try:
        currency = Currency.objects.get(id=currency_id)
        return {
            'currency': currency,
        }
    except Currency.DoesNotExist:
        return {'error': 'Moneda no encontrada.'}


def create_currency(name):
    """Create a new currency."""
    if not name or not name.strip():
        raise ValueError('El nombre de la moneda no puede estar vacío.')

    normalized_name = name.strip().upper()
    if Currency.objects.filter(name__iexact=normalized_name).exists():
        raise ValueError('El nombre de la moneda ya existe. Por favor, elige otro nombre.')

    currency = Currency.objects.create(name=normalized_name)
    return currency


def update_currency(currency_id, name):
    """Update an existing currency."""
    try:
        currency = Currency.objects.get(id=currency_id)
        if not name or not name.strip():
            raise ValueError('El nombre de la moneda no puede estar vacío.')

        normalized_name = name.strip().upper()
        currency_with_name = (
            Currency.objects
            .filter(name__iexact=normalized_name)
            .exclude(id=currency_id)
            .exists()
        )
        if currency_with_name:
            raise ValueError('El nombre de la moneda ya existe. Por favor, elige otro nombre.')

        currency.name = normalized_name
        currency.save()
        return currency
    except Currency.DoesNotExist:
        raise ValueError('Moneda no encontrada.')


def delete_currency(currency_id):
    """Delete a currency."""
    try:
        currency = Currency.objects.get(id=currency_id)
        currency.delete()
        return True
    except Currency.DoesNotExist:
        raise ValueError('Moneda no encontrada.')
