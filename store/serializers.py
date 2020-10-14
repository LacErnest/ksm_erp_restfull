from rest_framework import serializers
from .models import *


class InventoryMotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMotif
        fields = (
            'code',
            'description',
        )

class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        fields = (
            'code',
            'label',
            'description',
        )

class SourceMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceMovement
        fields = (
            'code',
            'wording',
            'apply_as_input',
            'output_application',
            'sequence_number',
            'business_transaction',
        )

class ArticleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleStore
        fields = (
            'stock_max',
            'stock_min',
            'replenishment_level',
            'unavailable',
            'physical_stock',
            'theoric_stock',
            'cumulative_entry',
            'cumulative_output',
            'last_inventory_date',
            'expiry_date',
            'manufactury_date',
            'product',
            'structure',
        )

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = (
            'code_ref',
            'object_ref',
            'movement_object_ref',
            'movement_date',
            'label',
            'notes',
            'exercice',
            'source_movement',
            'user',
            'store',
            'structure',
        )

class MovementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementDetail
        fields = (
            'sens_movement',
            'quantity_moved',
            'pre_movement_balance',
            'movement_date',
            'stock_movement',
            'article_store',
        )

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            'code',
            'open_date',
            'validation_date',
            'end_date',
            'fox',
            'validation_state',
            'inventory_type',
            'inventory_motif',
            'article_store',
        )

class InventoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryDetail
        fields = (
            'old_stock_quantity',
            'new_stock_quantity',
            'gap',
            'inventory',
            'article_store',
        )