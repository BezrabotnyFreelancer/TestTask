from django.urls import path, re_path, include
from .views import (
    TransactionListCreateAPIView,
    ReplenishmentCreateAPIView,
    ProfileDetailAPIView,
    CategoryListCreateAPIView,
    CategoryDeleteUpdateAPIView
)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('drf-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('profile/<uuid:pk>/', ProfileDetailAPIView.as_view(), name='api-profile-detail'),
    path('replenishment/', ReplenishmentCreateAPIView.as_view(), name='api-replenishment'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='api-transaction-list'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='api-category-list'),
    path('categories/<int:pk>/', CategoryDeleteUpdateAPIView.as_view(), name='api-category-manage'),
]