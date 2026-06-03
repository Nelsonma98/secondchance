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

    # Product
    path('products', views.products_panel, name='products_panel'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Ad
    path('ads/', views.ads_panel, name='ads_panel'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('ad/delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
]
