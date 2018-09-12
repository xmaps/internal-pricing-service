from django.urls import path

from . import views

urlpatterns = [
    path('price/', views.OrderPrice.as_view(), name='order_price'),
]
