from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('products/<int:product_id>/', product),
    path('declarations/<int:declaration_id>/', declaration),
]