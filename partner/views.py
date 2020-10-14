from django.contrib.auth.models import User
from django.db.models import Q, ProtectedError
from django.http import Http404
from rest_framework import permissions, viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from .models import *
from .permissions import *
from .serializers import *
from .services import *

class PartnerTypeViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les types de partenaire 
    """
    queryset = PartnerType.objects.all()
    serializer_class = PartnerTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'code', 'label']
    search_fields = ["id", "user__username", "code", "label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            print(repr(serializer.data))
            if not apps.is_installed('company'):
                post_company_partners_type(self.request.user.username, serializer.data, self.request.user.password)
        except IntegrityError as err:
            raise APIException(
                code=502,
                detail="Integrity error: {0}".format(err), 
            )

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class TypeAdresseViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les types d'adresses
    """
    queryset = TypeAdresse.objects.all()
    serializer_class = TypeAdresseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'code', 'label']
    search_fields = ["id", "user__username", "code", "label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class PartnerAdresseViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les addresses des partenaires
    """
    queryset = PartnerAdresse.objects.all()
    serializer_class = PartnerAdresseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user__username", "type_adresse__label", "partner__name", "longitude", "latitude"] 
    search_fields = ["id", "user__username", "type_adresse__label", "partner__name", "longitude", "latitude", "created_at", "update_at"] 
    ordering_fields = ["user__username", "type_adresse__label", "partner__name", "created_at", "update_at"] 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
        
class ContactViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les contacts
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user__username", "telephone", "email", "postal_code", "whatsapp_id", "partner__name"] 
    search_fields = ["user__username", "telephone", "email", "postal_code", "whatsapp_id", "partner__name"] 
    ordering_fields = ["user__username", "partner__name", "created_at", "update_at"] 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
        
class PriceViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les prix
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'code', 'label']
    search_fields = ["id", "user__username", "code", "label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
            
class EligiblePriceViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les prix auxquelles les partenaires sont elligibles
    """
    queryset = EligiblePrice.objects.all()
    serializer_class = EligiblePriceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'partner__name', 'price__label']
    search_fields = ["id", "user__username", "partner__name", "price__label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class ExemptTaxeViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les taxes auxquelles les partenaires sont  exemptés
    """
    queryset = ExemptTaxe.objects.all()
    serializer_class = ExemptTaxeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'partner__name', 'tax__label']
    search_fields = ["id", "user__username", "partner__name", "tax__label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class PartnerTaxViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les taxes 
    """
    queryset = PartnerTax.objects.all()
    serializer_class = PartnerTaxSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'code', 'label']
    search_fields = ["id", "user__username", "code", "label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
        
class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les methodes de paiement
    """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'code', 'label']
    search_fields = ["id", "user__username", "code", "label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class PartnerPaymentMethodViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les merhodes de paiement des partenaires
    """
    queryset = PartnerPaymentMethod.objects.all()
    serializer_class = PartnerPaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'partner__name', 'payment_method__label']
    search_fields = ["id", "user__username", "partner__name", "payment_method__label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class PartnerViewSet(viewsets.ModelViewSet):
    """
    Ce viewset fournit automatiquement les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les partenaires
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id", "user__username", "name", "matricule", "state", "social_reason", "juridical_form", "society",
        "city", "country", "creation_date", "partner_type__label", "created_at", "update_at"]
    search_fields = ["id", "user__username", "name", "matricule", "state", "social_reason", "juridical_form", "society",
        "city", "country", "creation_date", "partner_type__label", "created_at", "update_at"] 
    ordering_fields = ['user__username', 'created_at', 'update_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            if not apps.is_installed('company'):
                post_company_partners(self.request.user.username, serializer.data, self.request.user.password)
        except IntegrityError as err:
            raise APIException(
                code=502,
                detail="Integrity error: {0}".format(err), 
            )

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class UserList(generics.ListAPIView):
    """
    Ce generics fournit  les actions `list` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'is_staff', 'is_superuser']
    search_fields = ['username', 'is_staff', 'is_superuser']
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]

class UserDetail(generics.RetrieveAPIView):
    """
    Ce viewset fournit  l'action  `retrieve` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]

class SearchUser(APIView):
    """
    Rechercher un/des utilisateur(s), en fonction du nom d'utilisateur, de l'adresse email ou du nom.
    """
    permission_classes = [IsSuperUserAndIsAuthenticated]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            users = User.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            users = User.objects.filter(
                    Q(username__icontains=query) | 
                    Q(email__icontains=query) | 
                    Q(first_name__icontains=query)
                )
            if not users.exists():  
                raise Http404 
            
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

class SearchTax(APIView):
    """
    Rechercher une/des taxe(s), en fonction du code ou nom.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            taxes = PartnerTax.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            taxes = PartnerTax.objects.filter(Q(code__icontains=query) | Q(label__icontains=query) | Q(user__username__icontains=query))
            if not taxes.exists():  
                raise Http404 
            
        serializer = PartnerTaxSerializer(taxes, many=True, context={'request': request})
        return Response(serializer.data)
        
class SearchPrice(APIView):
    """
    Rechercher un/des type(s) de prix, en fonction du code ou nom.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            prices = Price.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            prices = Price.objects.filter(Q(code__icontains=query) | Q(label__icontains=query) | Q(user__username__icontains=query))
            if not prices.exists():  
                raise Http404 
        
        serializer = PriceSerializer(prices, many=True, context={'request': request})
        return Response(serializer.data)

class SearchPartnerType(APIView):
    """
    Rechercher un/des type(s) de partenaire, en fonction du code ou nom.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            partner_types = PartnerType.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            partner_types = PartnerType.objects.filter(Q(code__icontains=query) | Q(label__icontains=query) | Q(user__username__icontains=query))
            if not partner_types.exists():  
                raise Http404 
            
        serializer = PartnerTypeSerializer(partner_types, many=True, context={'request': request})
        return Response(serializer.data)

class SearchTypeAdresse(APIView):
    """
    Rechercher un/des type(s) d'adresse, en fonction du code, nom ou du nom d'utilisateur.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            type_adresses = TypeAdresse.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            type_adresses = TypeAdresse.objects.filter(Q(code__icontains=query) | Q(label__icontains=query) | Q(user__username__icontains=query))
            if not type_adresses.exists():  
                raise Http404 
            
        serializer = TypeAdresseSerializer(type_adresses, many=True, context={'request': request})
        return Response(serializer.data)

class SearchPaymentMethod(APIView):
    """
    Rechercher un/des methodes de paiement, en fonction du code, nom ou du nom d'utilisateur.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            payment_methods = PaymentMethod.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            payment_methods = PaymentMethod.objects.filter(Q(code__icontains=query) | Q(label__icontains=query) | Q(user__username__icontains=query))
            if not type_adresses.exists():  
                raise Http404 
            
        serializer = PaymentMethodSerializer(payment_methods, many=True, context={'request': request})
        return Response(serializer.data)

class SearchPartner(APIView):
    """
    Rechercher un/des partenaire(s), en fonction du matricule, du nom, du type, de la raison sociale, de la ville ou du pays .
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            partners = Partner.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            partners = Partner.objects.filter(
                    Q(matricule__icontains=query) | 
                    Q(name__icontains=query) | 
                    Q(partner_type__label__icontains=query) |
                    Q(social_reason__icontains=query) |
                    Q(city__icontains=query) |
                    Q(country__icontains=query) |
                    Q(user__username__icontains=query)
                )
            if not partners.exists():  
                raise Http404 
            
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class UserPartners(APIView):
    """
    Retrouver la liste des partenaires enregistrés par un utilisateur.
    """
    permission_classes = [IsSuperUserAndIsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.all()
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)        

class RegisteredPartners(APIView):
    """
    Retrouver la liste des partenaires que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        partners = (self.get_object(request.user.id)).partners.all()
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class TaxesNotAppliedToPartner(APIView):
    """
    Retrouvez la/les taxe(s) pour laquelle/lesquelles le partenaire est exempté
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        taxes = (self.get_object(id)).taxes.all()
        serializer = PartnerTaxSerializer(taxes, many=True, context={'request': request})
        return Response(serializer.data)

class PriceSubjectToAPartner(APIView):
    """
    Retrouvez le(s) prix pour le(s)quel(les) le partenaire est éligible. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        prices = (self.get_object(id)).prices.all()
        serializer = PriceSerializer(prices, many=True, context={'request': request})
        return Response(serializer.data)

class PaymentMethodsSubscribedToByAPartner(APIView):
    """
    Retrouvez la/les méthodes de paiement pour la(les)quelle(s) le partenaire à souscris. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        payment_methods = PartnerPaymentMethod.objects.filter(partner=self.get_object(id))
        serializer = PartnerPaymentMethodSerializer(payment_methods, many=True, context={'request': request})
        return Response(serializer.data)
        
class AddressesOfAPartner(APIView):
    """
    Retrouvez l'/les adresse(s) d'un partenaire. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partner_adresses = PartnerAdresse.objects.filter(partner=self.get_object(id))
        serializer = PartnerAdresseSerializer(partner_adresses, many=True, context={'request': request})
        return Response(serializer.data)
        
class ContactsOfAPartner(APIView):
    """
    Retrouvez le(s) contact(s) d'un partenaire. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        contacts = (self.get_object(id)).contacts.all()
        serializer = ContactSerializer(contacts, many=True, context={'request': request})
        return Response(serializer.data)

class TypeOfPartner(APIView):
    """
    Retrouvez le type de partenariat. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partner_type = (self.get_object(id)).partner_type
        serializer = PartnerTypeSerializer(partner_type, context={'request': request})
        return Response(serializer.data)

class PartnersNotSubjectToATax(APIView):
    """
    Retrouvez les partenaires non assujetti à une taxe. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return PartnerTax.objects.get(id=id)
        except PartnerTax.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.all()
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class PartnersEligibleForAPrize(APIView):
    """
    Retrouvez les partenaires éligible à un prix. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Price.objects.get(id=id)
        except Price.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.all()
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)
        
class PartnersOfAnAddressType(APIView):
    """
    Retrouvez les partenaires en fonction du type de d'adresse. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return TypeAdresse.objects.get(id=id)
        except TypeAdresse.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.distinct().all()  
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class PartnersOfAnAddressType(APIView):
    """
    Retrouvez les partenaires en fonction du type de d'adresse. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return TypeAdresse.objects.get(id=id)
        except TypeAdresse.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.distinct().all()  
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class PartnersForAPaymentMethod(APIView):
    """
    Retrouvez les partenaires affiliés à une méthode de paiement. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return PaymentMethod.objects.get(id=id)
        except PaymentMethod.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.distinct().all()  
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfSimilarPartners(APIView):
    """
    Retrouvez la liste des partenaires de même type. 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return PartnerType.objects.get(id=id)
        except PartnerType.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        partners = (self.get_object(id)).partners.all()  
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)
