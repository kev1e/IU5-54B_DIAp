from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/items/', search_items),  # GET
    path('api/items/<int:item_id>/', get_item_by_id),  # GET
    path('api/items/<int:item_id>/update/', update_item),  # PUT
    path('api/items/<int:item_id>/update_image/', update_item_image),  # POST
    path('api/items/<int:item_id>/delete/', delete_item),  # DELETE
    path('api/items/create/', create_item),  # POST
    path('api/items/<int:item_id>/add_to_declaration/', add_item_to_declaration),  # POST

    # Набор методов для заявок
    path('api/declarations/', search_declarations),  # GET
    path('api/declarations/<int:declaration_id>/', get_declaration_by_id),  # GET
    path('api/declarations/<int:declaration_id>/update/', update_declaration),  # PUT
    path('api/declarations/<int:declaration_id>/update_status_user/', update_status_user),  # PUT
    path('api/declarations/<int:declaration_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/declarations/<int:declaration_id>/delete/', delete_declaration),  # DELETE

    # Набор методов для м-м
    path('api/declarations/<int:declaration_id>/update_item/<int:item_id>/', update_item_in_declaration),  # PUT
    path('api/declarations/<int:declaration_id>/delete_item/<int:item_id>/', delete_item_from_declaration),  # DELETE

    # Набор методов пользователей
    path('api/users/register/', register), # POST
    path('api/users/login/', login), # POST
    path('api/users/logout/', logout), # POST
    path('api/users/<int:user_id>/update/', update_user) # PUT
]
