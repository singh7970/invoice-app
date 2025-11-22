from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_invoice, name='create_invoice'),
    path('master-data/', views.master_data, name='master_data'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
