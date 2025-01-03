from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:pk>/', views.product_detail, name='product detail'),
    path('update-item/', views.update_item, name='update item'),
    path('process-order/', views.process_order, name='process order'),
]
