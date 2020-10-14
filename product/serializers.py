from rest_framework import serializers
from rest_framework.reverse import reverse
from product.models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    list_of_products_described_in_a_language = serializers.HyperlinkedIdentityField(view_name='list_of_products_described_in_a_language', lookup_field='id')
    list_of_categories_described_in_a_language = serializers.HyperlinkedIdentityField(view_name='list_of_categories_described_in_a_language', lookup_field='id')

    class Meta:
        model = Language
        fields = ['url', 'id', 'user', 'code', 'name', 'is_default', 'created_at', 'update_at',
            'list_of_products_described_in_a_language', 'list_of_categories_described_in_a_language']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    list_of_products_in_a_category = serializers.HyperlinkedIdentityField(view_name='list_of_products_in_a_category', lookup_field='id')
    list_of_category_descriptions = serializers.HyperlinkedIdentityField(view_name='list_of_category_descriptions', lookup_field='id')
    list_of_subcategories = serializers.HyperlinkedIdentityField(view_name='list_of_subcategories', lookup_field='id')
    category_parent = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Category.objects.all(), slug_field='name', label="Catégorie Parent")
    code = serializers.CharField(max_length=6, min_length=6, allow_null=True, required=False, validators=[UniqueValidator(queryset=Category.objects.all())],
        help_text="Personnaliser votre code, mais nous vous conseillons de nous laisser s'en charger")
    class Meta:        
        model = Category 
        fields = ['url', 'id', 'user', 'code', 'name', 'image', 'category_parent', 'update_code', 
            'update_code_product', 'created_at', 'update_at', 'list_of_products_in_a_category', 
            'list_of_category_descriptions', 'list_of_subcategories']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class CategoryDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    language = serializers.SlugRelatedField(many=False, queryset=Language.objects.all(), slug_field='name', label="Langue")
    category = serializers.SlugRelatedField(many=False, queryset=Category.objects.all(), slug_field='name', label="Catégorie")

    class Meta:
        model = CategoryDescription
        fields = ['url', 'id', 'user', 'specification', 'description', 'language', 'category', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ConditioningSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    packaged_products = serializers.HyperlinkedIdentityField(view_name='packaged_products', lookup_field='id')

    class Meta:
        model = Conditioning
        fields = ['url', 'id', 'user', 'name', 'description', 'quantity', 'created_at', 'update_at', 'packaged_products']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    language = serializers.SlugRelatedField(many=False, queryset=Language.objects.all(), slug_field='name', label="Langue")
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")

    class Meta:
        model = ProductDescription
        fields = ['url', 'id', 'user', 'specification', 'description', 'language', 'product', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")

    class Meta:
        model = ProductDetail
        fields = ['url', 'id', 'user', 'model', 'mark', 'weight',
                    'conservation', 'origin', 'composition', 'product', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    category = serializers.SlugRelatedField(many=False, queryset=Category.objects.all(), slug_field='name', label="Catégorie")
    product_taxes_list = serializers.HyperlinkedIdentityField(view_name='product_taxes_list', lookup_field='id')
    product_category = serializers.HyperlinkedIdentityField(view_name='product_category', lookup_field='id')
    product_detail = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='id')
    product_pricing = serializers.HyperlinkedIdentityField(view_name='product_pricing', lookup_field='id')
    product_illustration_list = serializers.HyperlinkedIdentityField(view_name='product_illustration_list', lookup_field='id')
    product_description_list = serializers.HyperlinkedIdentityField(view_name='product_description_list', lookup_field='id')

    product_packagings_list = serializers.HyperlinkedIdentityField(view_name='product_packagings_list', lookup_field='id')

    #code = serializers.CharField(max_length=10, min_length=10, allow_null=True, required=False, label="Code", help_text="Personnaliser votre code, mais nous vous conseillons de nous laisser s'en charger")
    code = serializers.CharField(max_length=10, min_length=10, allow_null=True, required=False, validators=[UniqueValidator(queryset=Category.objects.all())],
        help_text="Personnaliser votre code, mais nous vous conseillons de nous laisser s'en charger")

    class Meta:
        model = Product
        fields = ['url', 'id', 'user', 'code', 'name', 'update_code', 'category', 'created_at', 
            'update_at', 'product_taxes_list', 'product_category', 'product_detail', 'product_pricing', 'product_illustration_list', 'product_description_list', 'product_packagings_list']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'taxes', 'pricing']
        write_only_fields = ['conditioning_purchase', 'conditioning_sale']

class TaxSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    taxed_products = serializers.HyperlinkedIdentityField(view_name='taxed_products', lookup_field='id')

    class Meta:
        model = Tax
        fields = ['url', 'id', 'user', 'name', 'value', 'description', 'created_at', 'update_at', 'taxed_products']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductTaxationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")
    tax = serializers.SlugRelatedField(many=False, queryset=Tax.objects.all(), slug_field='name', label="Taxe")

    class Meta:
        model = ProductTaxation
        fields = ['url', 'id', 'user', 'product', 'tax', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductPackagingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")
    conditioning = serializers.SlugRelatedField(many=False, queryset=Conditioning.objects.all(), slug_field='name', label="Conditionement")

    class Meta:
        model = ProductPackaging
        fields = ['url', 'id', 'user', 'product', 'conditioning', 'type_packaging', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class PricingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")

    class Meta:
        model = Pricing 
        fields = ['url', 'id', 'user', 'average_price','cost_price', 'unit_pricing', 'percentage_expence', 
                    'percentage_margin_rate', 'percentage_brand_taxes', 'half_wholesale_price','wholesale_price', 
                    'percentage_half_big_price', 'percentage_wholesale_price', 'total_accumulated_price', 'type_pricing', 
                    'product', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ProductIllustrationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.SlugRelatedField(many=False, queryset=Product.objects.all(), slug_field='name', label="Produit")

    class Meta:
        model = ProductIllustration
        fields = ['url', 'id', 'user', 'illustration', 'type_illustration', 'product', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_user-detail', lookup_field='pk')
    user_products = serializers.HyperlinkedIdentityField(view_name='user_products', lookup_field='id')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'user_products']
