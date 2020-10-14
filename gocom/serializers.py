from rest_framework import serializers
from rest_framework.reverse import reverse
from gocom.models import *
from django.contrib.auth.models import User

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Currency
        fields = ("__all__") 

class BusinessTransactionOriginSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:        
        model = BusinessTransactionOrigin 
        fields = ("__all__") 

class BusinessTransactionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BusinessTransaction
        fields = ("__all__") 

class BusinessTransactionDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    packaged_products = serializers.HyperlinkedIdentityField(view_name='packaged_products', lookup_field='id')

    class Meta:
        model = BusinessTransactionDetail
        fields = ("__all__") 
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_user-detail', lookup_field='pk')
    user_products = serializers.HyperlinkedIdentityField(view_name='user_products', lookup_field='id')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'user_products']
    
