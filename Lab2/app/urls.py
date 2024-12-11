from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('items/<int:item_id>/', item_details, name="item_details"),
    path('items/<int:item_id>/add_to_declaration/', add_item_to_draft_declaration, name="add_item_to_draft_declaration"),
    path('declarations/<int:declaration_id>/delete/', delete_declaration, name="delete_declaration"),
    path('declarations/<int:declaration_id>/', declaration)
]
