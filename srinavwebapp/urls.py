from django.urls import path
from . import views

urlpatterns = [
    # Home & Product Pages
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Seller Routes
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/products/add/', views.seller_add_product, name='seller_add_product'),
    path('seller/products/<int:product_id>/edit/', views.seller_edit_product, name='seller_edit_product'),
    path('seller/products/<int:product_id>/delete/', views.seller_delete_product, name='seller_delete_product'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
]