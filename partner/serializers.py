from rest_framework import serializers, status 
from rest_framework.reverse import reverse
from partner.models import *
from django.contrib.auth.models import User

class PartnerTypeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    list_of_similar_partners = serializers.HyperlinkedIdentityField(view_name='list_of_similar_partners', lookup_field='id')

    class Meta:
        model = PartnerType
        fields = ['url', 'id', 'user', 'code', 'label', 'description', 'created_at', 'update_at', 'list_of_similar_partners']
        
class TypeAdresseSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partners_of_an_address_type = serializers.HyperlinkedIdentityField(view_name='partners_of_an_address_type', lookup_field='id')

    class Meta:
        model = TypeAdresse
        fields = ['url', 'id', 'user', 'code', 'label', 'description', 'created_at', 'update_at', 'partners_of_an_address_type']

class PartnerAdresseSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner = serializers.SlugRelatedField(many=False,  queryset=Partner.objects.all(), slug_field='name', label="Partenaire associé")
    type_adresse = serializers.SlugRelatedField(many=False, queryset=TypeAdresse.objects.all(), slug_field='label', label="Type d'adress associé")

    class Meta:
        model = PartnerAdresse
        fields = ['url', 'id', 'user', 'longitude','latitude','default_delivery_address', 'partner', 'type_adresse', 'created_at', 'update_at']

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner = serializers.SlugRelatedField(many=False, queryset=Partner.objects.all(), slug_field='name', label="Partenaire associé")

    class Meta:
        model = Contact
        fields = ['url', 'id', 'user', 'name', 'telephone', 'email', 'fax', 'postal_code', 'web_site', 'whatsapp_id', 
                    'partner', 'created_at', 'update_at']

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partners_elligible_for_a_prize = serializers.HyperlinkedIdentityField(view_name='partners_elligible_for_a_prize', lookup_field='id')

    class Meta:
        model = Price
        fields = ['url', 'id', 'user', 'code', 'label', 'description', 'created_at', 'update_at', 'partners_elligible_for_a_prize']

class EligiblePriceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner = serializers.SlugRelatedField(many=False, queryset=Partner.objects.all(), slug_field='name', label="Partenaire associé")
    price = serializers.SlugRelatedField(many=False, queryset=Price.objects.all(), slug_field='label', label="Prix associé")

    class Meta:
        model = EligiblePrice
        fields = ['url', 'id', 'user', 'partner', 'price', 'created_at', 'update_at']

class ExemptTaxeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner = serializers.SlugRelatedField(many=False, queryset=Partner.objects.all(), slug_field='name', label="Partenaire associé")
    tax = serializers.SlugRelatedField(many=False, queryset=PartnerTax.objects.all(), slug_field='label', label="Taxe associée")

    class Meta:
        model = ExemptTaxe
        fields = ['url', 'id', 'user', 'partner', 'tax', 'created_at', 'update_at']

class PartnerTaxSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partners_not_subject_to_a_tax = serializers.HyperlinkedIdentityField(view_name='partners_not_subject_to_a_tax', lookup_field='id')

    class Meta:
        model = PartnerTax
        fields = ['url', 'id', 'user', 'code', 'label', 'description', 'created_at', 'update_at', 'partners_not_subject_to_a_tax']

class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partners_for_a_payment_method = serializers.HyperlinkedIdentityField(view_name='partners_for_a_payment_method', lookup_field='id')

    class Meta:
        model = PaymentMethod
        fields = ['url', 'id', 'user', 'code', 'label', 'image', 'description', 'created_at', 'update_at', 'partners_for_a_payment_method']

class PartnerPaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner = serializers.SlugRelatedField(many=False, queryset=Partner.objects.all(), slug_field='name', label="Partenaire associé")
    payment_method = serializers.SlugRelatedField(many=False, queryset=PaymentMethod.objects.all(), slug_field='label', label="Moyen de payement associé")

    class Meta:
        model = PartnerPaymentMethod
        fields = ['url', 'id', 'user', 'partner', 'payment_method', 'value', 'created_at', 'update_at']
        
class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    partner_type = serializers.SlugRelatedField(many=False, queryset=PartnerType.objects.all(), slug_field='label', label="Type de partenariat")
    taxes_not_applied_to_partner = serializers.HyperlinkedIdentityField(view_name='taxes_not_applied_to_partner', lookup_field='id')
    price_subject_to_a_partner = serializers.HyperlinkedIdentityField(view_name='price_subject_to_a_partner', lookup_field='id')
    type_of_partner = serializers.HyperlinkedIdentityField(view_name='type_of_partner', lookup_field='id')
    addresses_of_a_partner = serializers.HyperlinkedIdentityField(view_name='addresses_of_a_partner', lookup_field='id')
    contacts_of_a_partner = serializers.HyperlinkedIdentityField(view_name='contacts_of_a_partner', lookup_field='id')
    payment_methods_subscribed_to_by_a_partner = serializers.HyperlinkedIdentityField(view_name='payment_methods_subscribed_to_by_a_partner', lookup_field='id')

    class Meta:
        model = Partner
        fields = ['url', 'id', 'user', 'name', 'matricule', 'state', 'photo', 'social_reason', 'juridical_form', 
                    'society', 'description', 'family', 'city', 'country', 'creation_date', 'partner_type', 
                    'created_at', 'update_at', 'partner_type', 'taxes_not_applied_to_partner', 'price_subject_to_a_partner',
                    'type_of_partner', 'addresses_of_a_partner', 'contacts_of_a_partner', 'payment_methods_subscribed_to_by_a_partner']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='partner_user-detail', lookup_field='pk')
    user_partners = serializers.HyperlinkedIdentityField(view_name='user_partners', lookup_field='id')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'user_partners']
        
