from django.urls import path
from . import views
from django.contrib. auth import views as auth_views

urlpatterns = [
    path('', views.product_list, name = 'product_list'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/update/<int:product_id>/', views.update_product, name='update_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]