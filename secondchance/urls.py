"""secondchance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views as shop_views
from panel import views as panel_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # SHOP
    path('', shop_views.home, name='home'),

    path('product/<int:product_id>/', shop_views.product, name='product'),

    # PANEL
    path('panel/', panel_views.panel, name='panel'),

    path('panel/login/', panel_views.login, name='login'),

    # Category
    path('panel/categories/', panel_views.categories_panel, name='categories_panel'),

    path('panel/category/create/', panel_views.create_category, name='create_category'),

    path('panel/category/edit/<int:category_id>/', panel_views.edit_category, name = 'edit_category'),

    path('panel/category/delete/<int:category_id>/', panel_views.delete_category, name='delete_category'),

    # Product
    path('panel/products', panel_views.products_panel, name='products_panel'),

    path('panel/product/create/', panel_views.create_product, name='create_product'),

    path('panel/product/edit/<int:product_id>/', panel_views.edit_product, name = 'edit_product'),

    path('panel/product/delete/<int:product_id>/', panel_views.delete_product, name='delete_product'),

    # Ad
    path('panel/ads', panel_views.ads_panel, name='ads_panel'),

    path('panel/ad/create/', panel_views.create_ad, name='create_ad'),

    path('panel/ad/edit/<int:ad_id>/', panel_views.edit_ad, name = 'edit_ad'),

    path('panel/ad/delete/<int:ad_id>/', panel_views.delete_ad, name='delete_ad'),
]
