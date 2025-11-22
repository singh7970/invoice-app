from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_invoice, name='create_invoice'),
    path('master-data/', views.master_dashboard, name='master_dashboard'),
    path('master-data/senders/', views.sender_list, name='sender_list'),
    path('master-data/clients/', views.client_list, name='client_list'),
    path('master-data/products/', views.product_list, name='product_list'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
