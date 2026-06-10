from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Category
    path('categories/', views.categories_panel, name='categories_panel'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    # Currency
    path('currencies/', views.currencies_panel, name='currencies_panel'),
    path('currency/create/', views.create_currency, name='create_currency'),
    path('currency/edit/<int:currency_id>/', views.edit_currency, name='edit_currency'),
    path('currency/delete/<int:currency_id>/', views.delete_currency, name='delete_currency'),

    # Product
    path('products/', views.products_panel, name='products_panel'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Ad
    path('ads/', views.ads_panel, name='ads_panel'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('ad/delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),

    # User
    path('profile/username/', views.update_profile_username, name='update_profile_username'),
    path('profile/password/', views.update_profile_password, name='update_profile_password'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('users/create/', views.create_user, name='create_user'),
    path('', views.panel, name='panel' ),
]
