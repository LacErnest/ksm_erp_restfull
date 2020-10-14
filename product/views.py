from django.contrib.auth.models import User
from django.db.models import Q, ProtectedError
from django.http import Http404
from rest_framework import permissions, viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .permissions import *
from .serializers import *
from rest_framework_api_key.permissions import HasAPIKey

class LanguageViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les langues
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "code", "name", "is_default", "created_at", "update_at"] 
    ordering_fields = ("__all__")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

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
        
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les catégories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id", "user", "code", "name", "update_code", "update_code_product", "category_parent", "created_at", "update_at"] 
    search_fields = ["id", "user__username", "code", "name", "update_code", "update_code_product", "category_parent__name", "created_at", "update_at"] 
    ordering_fields = ["id", "user", "code", "name", "update_code", "update_code_product", "category_parent", "created_at", "update_at"] 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        try:
            serializer.save()
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

    def list(self, request, *args, **kwargs):
        no_paginate = request.GET.get('nopaginate')  
        if no_paginate:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class CategoryDescriptionViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les descriptions de categorie
    """
    queryset = CategoryDescription.objects.all()
    serializer_class = CategoryDescriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "language__name", "category__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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
       
class ConditioningViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les packages
    """
    queryset = Conditioning.objects.all()
    serializer_class = ConditioningSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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
        
class ProductDescriptionViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les descriptions de produit
    """
    queryset = ProductDescription.objects.all()
    serializer_class = ProductDescriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "language__name", "product__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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
        
class ProductViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les produits
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "code", "name", "update_code", "category__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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
    
    def list(self, request, *args, **kwargs):
        no_paginate = request.GET.get('nopaginate')  
        if no_paginate:
            products = Product.objects.all()
            serializer = CategorySerializer(products, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class TaxViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les taxes
    """
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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

class ProductTaxationViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour affecter des taxes aux produits
    """
    queryset = ProductTaxation.objects.all()
    serializer_class = ProductTaxationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "product__name", "tax__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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

class ProductPackagingViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les packagings des produits
    """
    queryset = ProductPackaging.objects.all()
    serializer_class = ProductPackagingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "product__name", "conditioning__name", "type_conditioning" "created_at", "update_at"] 
    ordering_fields = ("__all__")
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
        
class PricingViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les tarifs des produits
    """
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "type_pricing", "product__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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

class ProductDetailViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les details des produits
    """
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("__all__")
    search_fields = ["id", "user__username", "product__name", "created_at", "update_at"] 
    ordering_fields = ("__all__")
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

class ProductIllustrationViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les illustrations des produits
    """
    queryset = ProductIllustration.objects.all()
    serializer_class = ProductIllustrationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id", "user", "type_illustration", "product", "created_at", "update_at"] 
    search_fields = ["id", "user__username", "type_illustration", "product__name", "created_at", "update_at"] 
    ordering_fields = ["id", "user", "type_illustration", "product", "created_at", "update_at"] 
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

class UserList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'is_staff', 'is_superuser']
    search_fields = ['username', 'is_staff', 'is_superuser']
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]



class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  l'action  `retrieve` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]

class ListOfProductsDescribedInALanguage(APIView):
    """
    Retrouvez la liste des produits décrits dans une langue
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Language.objects.get(id=id)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        products = (self.get_object(id)).products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfCategoriesDescribedInALanguage(APIView):
    """
    Retrouvez la liste des catégories décrites dans une langue
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Language.objects.get(id=id)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        categories = (self.get_object(id)).categories.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfSubcategories(APIView):
    """
    Retrouvez la liste des sous catégorie d'une catégorie
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        subcategories = (self.get_object(id)).subcategories.all()
        serializer = CategorySerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfProductsInACategory(APIView):
    """
    Retrouvez la liste des produits d'une catégorie
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        products = (self.get_object(id)).products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfCategoryDescriptions(APIView):
    """
    Retrouvez la liste des descriptions d'une catégorie  
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        category_descriptions = (self.get_object(id)).category_descriptions.all()
        serializer = CategoryDescriptionSerializer(category_descriptions, many=True, context={'request': request})
        return Response(serializer.data)

class DescriptionOfACategoryInALanguage(APIView):
    """
    Retrouvez la description d'une catégorie  dans une langue 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, code, format=None):
        category_descriptions = (self.get_object(id)).category_descriptions.filter(language__code=code)
        if not category_descriptions.exists():
            raise Http404
        serializer = CategoryDescriptionSerializer(category_descriptions, many=True, context={'request': request})
        return Response(serializer.data)
    
class ProductTaxList(APIView):
    """
    Retrouvez la liste de taxes d'un produit
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        taxes = (self.get_object(id)).taxes.all()
        serializer = TaxSerializer(taxes, many=True, context={'request': request})
        return Response(serializer.data)

class ProductCategory(APIView):
    """
    Retrouvez la category d'un produit
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        category = (self.get_object(id)).category
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

class ProductDetail(APIView):
    """
    Retrouvez le détails d'un produit 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product_detail = (self.get_object(id)).product_detail
        serializer = ProductDetailSerializer(product_detail, context={'request': request})
        return Response(serializer.data)

class ProductPricing(APIView):
    """
    Retrouvez le tarif d'un produit à l'achat/ à la vente ou les deux 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        fare_type = request.GET.get('fare_type')
        if fare_type:
            pricing = (self.get_object(id)).pricing.filter(type_pricing=fare_type)
        else:
            pricing = (self.get_object(id)).pricing.all()
        serializer = PricingSerializer(pricing, many=True, context={'request': request})
        return Response(serializer.data)

class ProductIllustrationList(APIView):
    """
    Retrouvez la liste des illustrations d'un produit
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product_illustrations = (self.get_object(id)).product_illustrations.all()
        serializer = ProductIllustrationSerializer(product_illustrations, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDescriptionList(APIView):
    """
    Retrouvez la liste des descriptions d'un produit
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product_descriptions = (self.get_object(id)).product_descriptions.all()
        serializer = ProductDescriptionSerializer(product_descriptions, many=True, context={'request': request})
        return Response(serializer.data)

class ProductPackagingList(APIView):
    """
    Retrouvez la liste des packagings d'un produit
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        conditionnings = (self.get_object(id)).conditionnings.all()
        serializer = ConditioningSerializer(conditionnings, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDescriptionInOneLanguage(APIView):
    """
    Retrouvez la description d'un produit dans une langue
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, code, format=None):
        product_descriptions = (self.get_object(id)).product_descriptions.filter(language__code=code)
        if not product_descriptions.exists():
            raise Http404
        serializer = ProductDescriptionSerializer(product_descriptions, many=True, context={'request': request})
        return Response(serializer.data)
        
class TaxedProducts(APIView):
    """
    Retrouvez la liste des produits soumis à une taxe
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Tax.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        products = (self.get_object(id)).products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class PackagedProducts(APIView):
    """
    Retrouvez la liste des produits soumis à un packaging 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Conditioning.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        conditioning = self.get_object(id)
        products = Product.objects.filter(Q(conditioning_purchase=conditioning) | Q(conditioning_sale=conditioning))
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class SearchProduct(APIView):
    """
    Rechercher un/des produit(s), en fonction du code, nom, packaging ou le nom d'une catégorie
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            products = Product.objects.all()
        else:
            # la requête n'est pas sensible à la casse.
            products = Product.objects.filter(code__icontains=query)
            if not products.exists():    
                products = Product.objects.filter(name__icontains=query)
            if not products.exists():
                products = Product.objects.filter(category__name__icontains=query)
            if not products.exists():    
                products = Product.objects.filter(conditioning_purchase__name__icontains=query)
            if not products.exists():     
                products = Product.objects.filter(conditioning_sale__name__icontains=query)
            if not products.exists():  
                raise Http404 
            
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class SearchCategory(APIView):
    """
    Rechercher une/des catégorie(s), en fonction du code, nom.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            categories = Category.objects.all()
        else:
            # la requête n'est pas sensible à la casse.
            categories = Category.objects.filter(code__icontains=query)
            if not categories.exists():    
                categories = Category.objects.filter(name__icontains=query)
            if not categories.exists():  
                raise Http404 
            
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class SearchTax(APIView):
    """
    Rechercher une/des taxe(s), en fonction du nom.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        query = request.GET.get('query')
        if not query:
            taxes = Tax.objects.all()
        else:
            # la requête n'est pas sensible à la casse.    
            taxes = Tax.objects.filter(name__icontains=query)
            if not taxes.exists():  
                raise Http404 
            
        serializer = TaxSerializer(taxes, many=True, context={'request': request})
        return Response(serializer.data)

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
            users = User.objects.filter(username__icontains=query)
            if not users.exists():  
                users = User.objects.filter(email__icontains=query)
            if not users.exists():  
                users = User.objects.filter(first_name__icontains=query)
            if not users.exists():  
                raise Http404 
            
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

class UserProducts(APIView):
    """
    Retrouver la liste des produits enregistrés par utilisateur.
    """
    permission_classes = [IsSuperUserAndIsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        products = (self.get_object(id)).products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredLanguage(APIView):
    """
    Retrouver la liste des langues que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        languages = (self.get_object(request.user.id)).product_language.all()
        serializer = LanguageSerializer(languages, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredCategory(APIView):
    """
    Retrouver la liste des catégories que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        categories = (self.get_object(request.user.id)).categories.all()
        serializer = CqtegorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredCategoryDescription(APIView):
    """
    Retrouver la liste des descriptions des catégories que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_category_descriptions = (self.get_object(request.user.id)).product_category_descriptions.all()
        serializer = CategoryDescriptionSerializer(product_category_descriptions, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredConditioning(APIView):
    """
    Retrouver la liste des packagings que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_packagings = (self.get_object(request.user.id)).product_packagings.all()
        serializer = ConditioningSerializer(product_packagings, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProductDescription(APIView):
    """
    Retrouver la liste des descriptions des produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_product_descriptions = (self.get_object(request.user.id)).product_product_descriptions.all()
        serializer = ProductDescriptionSerializer(product_product_descriptions, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProduct(APIView):
    """
    Retrouver la liste des produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        products = (self.get_object(request.user.id)).products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredTax(APIView):
    """
    Retrouver la liste des taxes que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_taxes = (self.get_object(request.user.id)).product_taxes.all()
        serializer = TaxSerializer(product_taxes, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProductTaxation(APIView):
    """
    Retrouver la liste des taxes assignées aux produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_product_taxations = (self.get_object(request.user.id)).product_product_taxations.all()
        serializer = ProductTaxationSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProductPackaging(APIView):
    """
    Retrouver la liste des packagings des produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_product_packagings = (self.get_object(request.user.id)).product_product_packagings.all()
        serializer = ProductPackagingSerializer(product_product_packagings, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredPricing(APIView):
    """
    Retrouver la liste des tarifications que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_pricing = (self.get_object(request.user.id)).product_pricing.all()
        serializer = PricingSerializer(product_pricing, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProductDetail(APIView):
    """
    Retrouver la liste des details des produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_product_details = (self.get_object(request.user.id)).product_product_details.all()
        serializer = ProductDetailSerializer(product_product_details, many=True, context={'request': request})
        return Response(serializer.data)

class RegisteredProductIllustration(APIView):
    """
    Retrouver la liste des illustrations des produits que l'utilisateur connecté a enregistré.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        product_product_illustrations = (self.get_object(request.user.id)).product_product_illustrations.all()
        serializer = ProductIllustrationSerializer(product_product_illustrations, many=True, context={'request': request})
        return Response(serializer.data)
        
