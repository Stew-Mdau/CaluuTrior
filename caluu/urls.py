from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- Public & Product Management ---
    path('', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/update/<int:product_id>/', views.update_product, name='update_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # --- Direct Buy (Buy Now) ---
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),

    # --- Shopping Cart Logic ---
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/reduce/<int:item_id>/', views.reduce_cart_item, name='reduce_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    # --- Customer Order Management & Payment Notifications ---
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    # New paths for marking payments as sent:
    path('orders/notify/<int:order_id>/', views.notify_payment, name='notify_payment'),
    path('orders/notify-batch/', views.notify_batch_payment, name='notify_batch_payment'),

    # --- Seller Dashboard ---
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('seller/confirm-all/<int:customer_id>/', views.confirm_all_orders, name='confirm_all_orders'),

    # --- Authentication ---
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]