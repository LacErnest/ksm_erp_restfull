from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class InventoryMotifView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InventoryMotifSerializer
    queryset = InventoryMotif.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class InventoryTypeView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InventoryTypeSerializer
    queryset = InventoryType.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class SourceMovementView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SourceMovementSerializer
    queryset = SourceMovement.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class ArticleStoreView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):   
    permission_classes = (IsAuthenticated, )
    serializer_class = ArticleStoreSerializer
    queryset = ArticleStore.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class StockMovementView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = StockMovementSerializer
    queryset = StockMovement.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class MovementDetailView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MovementDetailSerializer
    queryset = MovementDetail.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class InventoryView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []

class InventoryDetailView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InventoryDetailSerializer
    queryset = InventoryDetail.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        return []