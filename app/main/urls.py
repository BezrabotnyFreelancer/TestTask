from django.urls import path
from .views import (
    main_profile,
    replenishment,
    transactions_list,
    create_transaction,
    category_list_and_create,
    CategoryUpdateView,
    CategoryDeleteView
)

urlpatterns = [
    path('', main_profile, name='profile'),
    path('replenishment/', replenishment, name='replenishment_balance'),
    path('transactions/', transactions_list, name='transaction_list'),
    path('transactions/create/', create_transaction, name='transactions_create'),
    path('categories/', category_list_and_create, name='categories'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete')
]
