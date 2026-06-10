from .view_modules.auth import login, logout
from .view_modules.dashboard import (
    panel,
    update_profile_username,
    update_profile_password,
    delete_profile,
    create_user,
)
from .view_modules.category import categories_panel, create_category, edit_category, delete_category
from .view_modules.product import products_panel, create_product, edit_product, delete_product
from .view_modules.ad import ads_panel, create_ad, edit_ad, delete_ad
from .view_modules.currency import currencies_panel, create_currency, edit_currency, delete_currency
