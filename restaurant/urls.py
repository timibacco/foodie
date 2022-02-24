from django.urls import path
from restaurant.views import Dashboard, OrderDetails

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name= 'dashboard'),
    path('order-details/<int:pk>/', OrderDetails.as_view(), name = 'order-details'),
]