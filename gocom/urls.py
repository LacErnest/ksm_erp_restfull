from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gocom import views
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'business_transaction_origin', views.BusinessTransactionOriginViewSet)
router.register(r'business_transaction_detail', views.BusinessTransactionDetailViewSet)
router.register(r'business_transaction', views.BusinessTransactionViewSet)


urlpatterns = [
    # Les URL des API sont déterminées automatiquement par le routeur.
    path('', include(router.urls)),
    # URL personnalisées.
    path('users/', views.UserList.as_view(), name='gocom_user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='gocom_user-detail')
]
