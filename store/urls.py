from django.urls import include, path
from django.conf.urls import url
from .views import *

app_name = 'stock'

# router = routers.DefaultRouterWithSimpleViews()
# router.register('inventory-motif/',InventoryMotifView, basename='InventoryMotif')
# router.register('inventory-type/',InventoryTypeView, basename='InventoryType')
# router.register('source-movement/',SourceMovementView, basename='SourceMovement')
# router.register('article-store/',ArticleStoreView, basename='ArticleStore')
# router.register('stock-movement/',StockMovementView, basename='StockMovement')
# router.register('movement-detail/',MovementDetailView, basename='MovementDetail')
# router.register('inventory/',InventoryView, basename='Inventory')
# router.register('inventory-detail/',InventoryDetailView, basename='InventoryDetail')

urlpatterns = [
    path('inventory-motif/', InventoryMotifView.as_view(), name='stock.inventory_motif'),
    path('inventory-type/', InventoryTypeView.as_view(), name='stock.invetory_type'),
    path('source-movement/', SourceMovementView.as_view(), name='stock.source_movement'),
    path('article-store/', ArticleStoreView.as_view(), name='stock.article_store'),
    path('stock-movement/', StockMovementView.as_view(), name='stock.stock_movement'),
    path('movement-detail/', MovementDetailView.as_view(), name='stock.movement_detail'),
    path('inventory/', InventoryView.as_view(), name='stock.invetory'),
    path('inventory-detail/', InventoryDetailView.as_view(), name='stock.invetory_detail'),
]