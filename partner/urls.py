from django.urls import path, include
from rest_framework.routers import DefaultRouter
from partner import views
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets with it.
router = DefaultRouter()
<<<<<<< HEAD
#router.register(r'users', views.UserViewSet)
=======
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
router.register(r'partner_types', views.PartnerTypeViewSet)
router.register(r'type_adresses', views.TypeAdresseViewSet)
router.register(r'prices', views.PriceViewSet)
router.register(r'taxes', views.PartnerTaxViewSet)
router.register(r'payment_methods', views.PaymentMethodViewSet)
router.register(r'partners', views.PartnerViewSet)
router.register(r'exempt_taxes', views.ExemptTaxeViewSet)
router.register(r'partner_adresses', views.PartnerAdresseViewSet)
router.register(r'eligible_prices', views.EligiblePriceViewSet)
router.register(r'partner_payment_methods', views.PartnerPaymentMethodViewSet)
router.register(r'contacts', views.ContactViewSet)

# Les URL des API sont déterminées automatiquement par le routeur.
urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.UserList.as_view(), name='parner_user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='partner_user-detail'),
    path('users/<int:id>/partners', views.UserPartners.as_view(), name="user_partners"),
    path('search/users/', views.SearchUser.as_view(), name="search_user_partners"),
    path('search/taxes/', views.SearchTax.as_view(), name="search_partner_taxes"),
    path('search/partner_types/', views.SearchPartnerType.as_view(), name="search_partner_types"),
    path('search/prices/', views.SearchPrice.as_view(), name="search_prices"),
    path('search/partners/', views.SearchPartner.as_view(), name="search_partners"),
    path('search/type_adresses/', views.SearchTypeAdresse.as_view(), name="search_type_adresses"),
    path('registered/partners', views.RegisteredPartners.as_view(), name="registered_partners"),
    path('partners/<uuid:id>/taxes', views.TaxesNotAppliedToPartner.as_view(), name="taxes_not_applied_to_partner"),
    path('partners/<uuid:id>/prices', views.PriceSubjectToAPartner.as_view(), name="price_subject_to_a_partner"),
    path('partners/<uuid:id>/partner_type', views.TypeOfPartner.as_view(), name="type_of_partner"),
    path('partners/<uuid:id>/partner_adresses', views.AddressesOfAPartner.as_view(), name="addresses_of_a_partner"),
    path('partners/<uuid:id>/contacts', views.ContactsOfAPartner.as_view(), name="contacts_of_a_partner"),
    path('partners/<uuid:id>/payment_methods', views.PaymentMethodsSubscribedToByAPartner.as_view(), name="payment_methods_subscribed_to_by_a_partner"),
    path('taxes/<uuid:id>/partners', views.PartnersNotSubjectToATax.as_view(), name="partners_not_subject_to_a_tax"),
    path('prices/<uuid:id>/partners', views.PartnersEligibleForAPrize.as_view(), name="partners_elligible_for_a_prize"),
    path('partner_types/<uuid:id>/partners', views.ListOfSimilarPartners.as_view(), name="list_of_similar_partners"),
    path('type_adresses/<uuid:id>/partners', views.PartnersOfAnAddressType.as_view(), name="partners_of_an_address_type"),
    path('payment_methods/<uuid:id>/partners', views.PartnersForAPaymentMethod.as_view(), name="partners_for_a_payment_method"),
<<<<<<< HEAD
]

# Les URL des API sont déterminées automatiquement par le routeur.
urlpatterns = [
    path('', include(router.urls),  ),
=======
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
]