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

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les langues
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
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
        
class BusinessTransactionOriginViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les catégories
    """
    queryset = BusinessTransactionOrigin.objects.all()
    serializer_class = BusinessTransactionOriginSerializer
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

class BusinessTransactionViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les descriptions de categorie
    """
    queryset = BusinessTransaction.objects.all()
    serializer_class = BusinessTransactionSerializer
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
       
class BusinessTransactionDetailViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve`,
    `update` et `destroy` pour les packages
    """
    queryset = BusinessTransactionDetail.objects.all()
    serializer_class = BusinessTransactionDetailSerializer
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






