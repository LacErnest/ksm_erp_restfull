from django.urls import include, path
# from django.conf.urls import url
# from .views import *
from rest_framework import routers
from stock import views

app_name = 'stock'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'inventory-motifs',views.InventoryMotifViewSet)
router.register(r'inventory-types',views.InventoryTypeViewSet)
router.register(r'source-movements',views.SourceMovementViewSet)
router.register(r'article-stores',views.ArticleStoreViewSet)
router.register(r'stock-movements',views.StockMovementViewSet)
router.register(r'movement-details',views.MovementDetailViewSet)
router.register(r'inventories',views.InventoryViewSet)
router.register(r'inventory-details',views.InventoryDetailViewSet)

urlpatterns = [
	# Les URL des API sont déterminées automatiquement par le routeur.
    path('', include(router.urls), name="STOCK APIs"),
    # URL personnalisées.
    path('inventory-motifs/<uuid:id>', views.InventoryMotifDetail.as_view(), name="inventorymotif-detail"),
    path('inventory-types/<uuid:id>', views.InventoryTypeDetail.as_view(), name="inventorytype-detail"),
    path('source-movements/<uuid:id>', views.SourceMovementDetail.as_view(), name="sourcemovement-detail"),
    path('article-stores/<uuid:id>', views.ArticleStoreDetail.as_view(), name="articlestore-detail"),
    path('stock-movements/<uuid:id>', views.StockMovementDetail.as_view(), name="stockmovement-detail"),
    path('stock-movements/<uuid:id>/movement-details', views.ListOfMovementDetailsOfAMovement.as_view(), name="list_of_movement_details_of_a_stock_movement"),
    path('movement-details/<uuid:id>', views.MovementDetail.as_view(), name="movement-detail"),
    path('inventories/<uuid:id>', views.InventoryDetail.as_view(), name="inventory-detail"),
    path('inventories-details/<uuid:id>', views.InventoryPlusDetail.as_view(), name="inventoryplus-detail"),
    path('structures/<uuid:id>/inventory-motifs', views.ListOfInventoryMotifsInAStructure.as_view(), name="list_of_inventory_motifs_in_a_structure"),
    path('structures/<uuid:id>/inventory-types', views.ListOfInventoryTypesInAStructure.as_view(), name="list_of_inventory_types_in_a_structure"),
    path('structures/<uuid:id>/inventories', views.ListOfInventoriesInAStructure.as_view(), name="list_of_inventories_in_a_structure"),
    path('structures/<uuid:id>/inventories-pending', views.ListOfInventoriesInAStructurePending.as_view(), name="list_of_inventories_in_a_structure_pending"),
    path('structures/<uuid:id>/inventories-validate', views.ListOfInventoriesInAStructureValidate.as_view(), name="list_of_inventories_in_a_structure_validate"),
    path('structures/<uuid:id>/stock-movements', views.ListOfStockMovementInAStructure.as_view(), name="list_of_stock_movements_in_a_structure"),
    path('structures/<uuid:id>/stock-movements/<uuid:stockid>/movement-details', views.ListOfMovementDetailsOfAMovementInAStructure.as_view(), name="list_of_stock_movements_in_a_structure"),
    path('structures/<uuid:id>/source-movement', views.ListOfSourceMovementInAStructure.as_view(), name="list_of_source_movements_in_a_structure"),
    path('structures/<uuid:id>/article-stores', views.ListOfArticleStoreInAStructure.as_view(), name="list_of_article_stores_in_a_structure"),
    path('structures/<uuid:id>/article-stores-unavailable', views.ListOfArticleStoreUnavailableInAStructure.as_view(), name="list_of_article_stores_unavailable_in_a_structure"),
    path('structures/<uuid:id>/article-stores-under-replinishment', views.ListOfArticleStoreUnderReplenishmentInAStructure.as_view(), name="list_of_article_stores_underreplinishment_in_a_structure"),
    path('structures/<uuid:id>/article-stores-expired', views.ListOfArticleStoreExpiredInAStructure.as_view(), name="list_of_article_stores_expired_in_a_structure"),
    path('structures/<uuid:id>/article-stores-lesserthan/<int:value>', views.ListOfArticleStoreLesserThanInAStructure.as_view(), name="list_of_article_stores_lesser_than_a_value_in_a_structure"),
    path('structures/<uuid:id>/article-stores-lessorequal/<int:value>', views.ListOfArticleStoreLessOrEqualInAStructure.as_view(), name="list_of_article_stores_less_or_equal_a_value_in_a_structure"),
    path('structures/<uuid:id>/article-stores-equal/<int:value>', views.ListOfArticleStoreEqualInAStructure.as_view(), name="list_of_article_stores_equal_a_value_in_a_structure"),
    path('structures/<uuid:id>/article-stores-greatorequal/<int:value>', views.ListOfArticleStoreGreatOrEqualInAStructure.as_view(), name="list_of_article_stores_great_or_equal_a_value_in_a_structure"),
    path('structures/<uuid:id>/article-stores-greaterthan/<int:value>', views.ListOfArticleStoreGreaterThanInAStructure.as_view(), name="list_of_article_stores_greater_than_a_value_in_a_structure"),
    path('structures/<uuid:id>/article-stores-count', views.ListOfArticleStoreCountInAStructure.as_view(), name="list_of_article_stores_counts_in_a_structure"),
    path('structures/<uuid:id>/article-stores-value', views.ListOfArticleStoreValueInAStructure.as_view(), name="list_of_article_stores_value_in_a_structure"),

 	]