from django.db import migrations


def uppercase_currency_names(apps, schema_editor):
    Currency = apps.get_model('shop', 'Currency')

    for currency in Currency.objects.all().iterator():
        normalized_name = currency.name.strip().upper()
        if currency.name != normalized_name:
            currency.name = normalized_name
            currency.save(update_fields=['name'])


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_currency'),
    ]

    operations = [
        migrations.RunPython(
            uppercase_currency_names,
            migrations.RunPython.noop,
        ),
    ]
