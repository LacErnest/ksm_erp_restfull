from rest_framework import serializers
from .models import *
""" from company.models import *
from gocom.models import *
from product.models import * """
from django.contrib.auth.models import User


class InventoryMotifSerializer(serializers.HyperlinkedModelSerializer):
    structure = serializers.HyperlinkedIdentityField(view_name='company:structure', lookup_field='id')
    url = serializers.HyperlinkedIdentityField(view_name="stock:inventorymotif-detail", lookup_field='id')
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    class Meta:
        model = InventoryMotif
        fields = [
            'url',
            'code',
            'description',
            'structure',
            'created_at',
            'update_at',
        ]
        read_only_fields = ['created_at', 'update_at']

class InventoryTypeSerializer(serializers.HyperlinkedModelSerializer):
    structure = serializers.HyperlinkedIdentityField(view_name='company:structures-detail', lookup_field='id')
    url = serializers.HyperlinkedIdentityField(view_name="stock:inventorytype-detail", lookup_field='id')
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    class Meta:
        model = InventoryType
        fields = [
            'url',
            'code',
            'label',
            'description',
            'structure',
            'created_at',
            'update_at',
        ]
        read_only_fields = ['created_at', 'update_at']

class SourceMovementSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:sourcemovement-detail", lookup_field='id')
    structure = serializers.HyperlinkedIdentityField(view_name='company:structure', lookup_field='id')
    business_transaction = serializers.HyperlinkedIdentityField(view_name='gocom:business_transaction', lookup_field='id')
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    business_transaction = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=BusinessTransaction.objects.all(), slug_field='slug', label="Transaction associée")

    class Meta:
        model = SourceMovement
        fields = [
            'url',
            'code',
            'wording',
            'apply_as_input',
            'output_application',
            'business_transaction',
            'structure',
            'created_at',
            'update_at',
            'sequence_number',
        ]
        read_only_fields = ['created_at', 'update_at','sequence_number']

class ArticleStoreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:articlestore-detail", lookup_field='id')
    structure = serializers.HyperlinkedIdentityField(view_name='structure', lookup_field='id')
    product = serializers.HyperlinkedIdentityField(view_name='product', lookup_field='id')
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    product = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Product.objects.all(), slug_field='name', label="Produit associé")

    class Meta:
        model = ArticleStore
        fields = [
            'url',
            'stock_max',
            'stock_min',
            'replenishment_level',
            'physical_stock',
            'theoric_stock',
            'expiry_date',
            'manufactury_date',
            'product',
            'structure',
            'created_at',
            'update_at',
            'reference',
            'unavailable',
            'last_inventory_date',
        ]
        read_only_fields = ['created_at', 'update_at','reference','unavailable','last_inventory_date',]

class StockMovementSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:stockmovement-detail", lookup_field='id')
    structure = serializers.HyperlinkedIdentityField(view_name='company:structure', lookup_field='id')
    source_movement = serializers.HyperlinkedIdentityField(view_name='stock:structure', lookup_field='id')
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    source_movement = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=SourceMovement.objects.all(), slug_field='code', label="Source de mouvement associé")
    initiator = serializers.ReadOnlyField(source='initiator.username')
    list_of_movement_details_of_a_stock_movement = serializers.HyperlinkedIdentityField(view_name='stock:list_of_movement_details_of_a_stock_movement', lookup_field='id')
    class Meta:
        model = StockMovement
        fields = [
            'url',
            'code_ref',
            'object_ref',
            'movement_object_ref',
            'movement_date',
            'label',
            'notes',
            'exercice',
            'source_movement',
            'initiator',
            'structure',
            'list_of_movement_details_of_a_stock_movement',
        ]
        read_only_fields = ['created_at', 'update_at','code_ref','object_ref','movement_object_ref','movement_date','exercice']

class MovementDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:movement-detail", lookup_field='id')
    article_store = serializers.HyperlinkedIdentityField(view_name='stock:articlestore-detail', lookup_field='id')
    #stock_movement = serializers.HyperlinkedIdentityField(view_name='stock:stock_movement', lookup_field='id')
    stock_movement = serializers.HyperlinkedRelatedField(view_name='stock:stockmovement-detail', read_only=True)
    article_store = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=ArticleStore.objects.all(), slug_field='reference', label="Article en stock associé")
    stock_movement = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=StockMovement.objects.all(), slug_field='code_ref', label="Mouvement en stock associé")
    class Meta:
        model = MovementDetail
        fields = [
            'url',
            'id',
            'sens_movement',
            'quantity_moved',
            'movement_date',
            'stock_movement',
            'article_store',
        ]
        read_only_fields = ['created_at', 'update_at','code_ref','movement_date','id']
class InventorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:inventory-detail", lookup_field='id')
    article_store = serializers.HyperlinkedIdentityField(view_name='stock:article_store', lookup_field='id')
    article_store = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=ArticleStore.objects.all(), slug_field='reference', label="Article en stock associé")
    structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    structure = serializers.HyperlinkedIdentityField(view_name='company:structure', lookup_field='id')
    inventory_type = serializers.HyperlinkedIdentityField(view_name='stock:article_store', lookup_field='id')
    inventory_motif = serializers.HyperlinkedIdentityField(view_name='stock:article_store', lookup_field='id')
    inventory_type = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=InventoryMotif.objects.all(), slug_field='code', label="Motif associé")
    inventory_motif = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=InventoryType.objects.all(), slug_field='code', label="Type associé")
    class Meta:
        model = Inventory
        fields = [
            'url',
            'code',
            'open_date',
            'validation_date',
            'end_date',
            'fox',
            'validation_state',
            'inventory_type',
            'inventory_motif',
            'article_store',
            'structure',
        ]
        read_only_fields = ['created_at', 'update_at','fox','validation_date','open_date','end_date']
class InventoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="stock:inventoryplus-detail", lookup_field='id')
    article_store = serializers.HyperlinkedIdentityField(view_name='stock:article_store', lookup_field='id')
    article_store = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=ArticleStore.objects.all(), slug_field='reference', label="Article en stock associé")
    inventory = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Inventory.objects.all(), slug_field='name', label="Structure associée")
    inventory = serializers.HyperlinkedIdentityField(view_name='stock:inventory-detail', lookup_field='id')
    class Meta:
        model = InventoryDetail
        fields = [
            'url',
            'old_stock_quantity',
            'new_stock_quantity',
            'gap',
            'inventory',
            'article_store',
        ]
        read_only_fields = ['created_at', 'update_at','old_stock_quantity','gap',]

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff', 'is_superuser', ]