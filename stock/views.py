from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from .models import *
from .permissions import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import VALUE_CHOICES,MOVEMENT_CHOICES,STATUS_CHOICES

# Create your views here.

class InventoryMotifViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les motifs d'inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InventoryMotifSerializer
    queryset = InventoryMotif.objects.all()

    def perform_create(self, serializer):
        structures = Structure.objects.filter(user=self.request.user)
        #serializer(structure=structures)
        print(structures[0])
        serializer.save()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )


class InventoryTypeViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les types d'inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InventoryTypeSerializer
    queryset = InventoryType.objects.all()

    def perform_create(self, serializer):
        structures = Structure.objects.filter(user=self.request.user)
        #serializer(structure=structures)
        print(structures[0])
        serializer.save()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )

class SourceMovementViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les sources de mouvement
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = SourceMovementSerializer
    queryset = SourceMovement.objects.all()

    def perform_create(self, serializer):
        structures = Structure.objects.filter(user=self.request.user)
        #serializer(structure=structures)
        print(structures[0])
        serializer.save()
        serializer.save(sequence_number=SourceMovement.objects.all().count())

    def perform_update(self, serializer):
        try:
            serializer.save(sequence_number=self.sequence_number+1)
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )


class ArticleStoreViewSet(viewsets.ModelViewSet): 
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les articles en stock
    """ 
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ArticleStoreSerializer
    queryset = ArticleStore.objects.all()

    def perform_create(self, serializer):
        structures = Structure.objects.filter(user=self.request.user)
        #serializer(structure=structures)
        print(structures[0])
        print(serializer)
        serializer.save()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )

class StockMovementViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les mouvement de stock
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = StockMovementSerializer
    queryset = StockMovement.objects.all()

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )

class MovementDetailViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les détails de mouvement de stock
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MovementDetailSerializer
    queryset = MovementDetail.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            ) 
    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )

class InventoryViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les inventaires
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )

class InventoryDetailViewSet(viewsets.ModelViewSet):
    """
    Vous pouvez éffectuer les actions `list`, `create`, `retrieve` et
    `update` pour les détails d'inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InventoryDetailSerializer
    queryset = InventoryDetail.objects.all()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise APIException(
                code=500,
                detail="An internal error has occurred. Please try your request again.", 
            )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vous pouvez effectuer les actions `list`, `create`, `retrieve`,
    `update` pour les utilisateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserAndIsAuthenticated, ]

class InventoryTypeDetail(APIView):
    """
    Retrouvez les détails d'un type d'inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return InventoryType.objects.get(id=id)
        except InventoryType.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventory_type_detail = self.get_object(id)
        serializer = InventoryTypeSerializer(inventory_type_detail, context={'request': request})
        return Response(serializer.data)


class InventoryMotifDetail(APIView):
    """
    Retrouvez les détails d'un motif d'inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return InventoryMotif.objects.get(id=id)
        except InventoryMotif.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventory_motif_detail = self.get_object(id)
        serializer = InventoryMotifSerializer(inventory_motif_detail, context={'request': request})
        return Response(serializer.data)


class SourceMovementDetail(APIView):
    """
    Retrouvez les détails d'une source de mouvement
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return SourceMovement.objects.get(id=id)
        except SourceMovement.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        source_movement_detail = self.get_object(id)
        serializer = SourceMovementSerializer(source_movement_detail, context={'request': request})
        return Response(serializer.data)


class ArticleStoreDetail(APIView):
    """
    Retrouvez les détails d'un article en stock
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return ArticleStore.objects.get(id=id)
        except ArticleStore.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_store_detail = self.get_object(id)
        serializer = ArticleStoreSerializer(article_store_detail, context={'request': request})
        return Response(serializer.data)


class StockMovementDetail(APIView):
    """
    Retrouvez les détails d'un mouvement en stock
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return StockMovement.objects.get(id=id)
        except StockMovement.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        stock_movement_detail = self.get_object(id)
        serializer = StockMovementSerializer(stock_movement_detail, context={'request': request})
        return Response(serializer.data)

class ListOfMovementDetailsOfAMovement(APIView):
    """
    Retrouvez les détails d'un mouvement de stock plus en détail 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return StockMovement.objects.get(id=id)
        except StockMovement.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        stock_movement = self.get_object(id)
        movement_details = MovementDetail.objects.filter(stock_movement=stock_movement) 
        serializer = MovementDetailSerializer(movement_details, many=True, context={'request': request})
        return Response(serializer.data)

class MovementDetail(APIView):
    """
    Retrouvez les détails des détails d'un mouvement en stock
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return MovementDetail.objects.get(id=id)
        except MovementDetail.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        movement_detail = self.get_object(id)
        serializer = MovementDetailSerializer(movement_detail, context={'request': request})
        return Response(serializer.data)


class InventoryDetail(APIView):
    """
    Retrouvez les détails d'un inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Inventory.objects.get(id=id)
        except Inventory.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventory = self.get_object(id)
        serializer = InventorySerializer(inventory, context={'request': request})
        return Response(serializer.data)

class InventoryPlusDetail(APIView):
    """
    Retrouvez les détails des détails d'un inventaire
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return InventoryDetail.objects.get(id=id)
        except InventoryDetail.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventory_detail = self.get_object(id)
        serializer = InventoryDetailSerializer(inventory_detail, context={'request': request})
        return Response(serializer.data)

class ListOfInventoryMotifsInAStructure(APIView):
    """
    Retrouvez la liste des motifs d'inventaires  
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventorymotifs = (self.get_object(id)).inventorymotifs.all()
        serializer = InventoryMotifSerializer(inventorymotifs, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfInventoryTypesInAStructure(APIView):
    """
    Retrouvez la liste des types d'inventaires  
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventorytypes = (self.get_object(id)).inventorytypes.all()
        serializer = InventoryTypeSerializer(inventorytypes, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfInventoriesInAStructure(APIView):
    """
    Retrouvez la liste des inventaires  
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventories = (self.get_object(id)).inventories.all()
        serializer = InventorySerializer(inventories, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfInventoriesInAStructurePending(APIView):
    """
    Retrouvez la liste des inventaires en cours 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventories = (self.get_object(id)).inventories.filter(validation_state=STATUS_CHOICES[1][0]) #Pending
        serializer = InventorySerializer(inventories, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfInventoriesInAStructureValidate(APIView):
    """
    Retrouvez la liste des inventaires validés 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        inventories = (self.get_object(id)).inventories.filter(validation_state=STATUS_CHOICES[3][0]) #Succeeded
        serializer = InventorySerializer(inventories, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfStockMovementInAStructure(APIView):
    """
    Retrouvez la mouvements de stock 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        stock_movements = (self.get_object(id)).stock_movements.all() 
        serializer = StockMovementSerializer(stock_movements, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfMovementDetailsOfAMovementInAStructure(APIView):
    """
    Retrouvez les détails d'un mouvement de stock 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.filter(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        stock_movement = (self.get_object(id)).stock_movements.filter(stock_movement_id=request.stockid)
        movement_details = stock_movement.movement_details.all() 
        serializer = MovementDetailSerializer(movement_details, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfSourceMovementInAStructure(APIView):
    """
    Retrouvez les sources de mouvements de stock 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        source_movements = (self.get_object(id)).source_movements.all() 
        serializer = SourceMovementSerializer(source_movements, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreInAStructure(APIView):
    """
    Retrouvez les articles en stock d'une structure 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all() 
        serializer = ArticleStoreSerializer(article_stores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreUnavailableInAStructure(APIView):
    """
    Retrouvez les articles en rupture de stock d'une structure 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.filter(unavailable=VALUE_CHOICES[0][0]) #Yes
        serializer = ArticleStoreSerializer(article_stores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreUnderReplenishmentInAStructure(APIView):
    """
    Retrouvez les articles en rupture de stock d'une structure 
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.replenishment_level >= article_store.theoric_stock :
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreExpiredInAStructure(APIView):
    """
    Retrouvez les articles expirés de stock d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.expiry_date <= datetime.datetime.now() :
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreLesserThanInAStructure(APIView):
    """
    Retrouvez les articles en stock inférieure ou égale à une valeur d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.product.unit_pricing < request.value :
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreLessOrEqualInAStructure(APIView):
    """
    Retrouvez les articles en stock inférieure ou égale à une valeur d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self,id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.product.unit_pricing <= request.value :
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)


class ListOfArticleStoreGreaterThanInAStructure(APIView):
    """
    Retrouvez les articles en stock inférieure ou égale à une valeur d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.product.unit_pricing > request.value:
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)


class ListOfArticleStoreGreatOrEqualInAStructure(APIView):
    """
    Retrouvez les articles en stock inférieure ou égale à une valeur d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.product.unit_pricing >= request.value:
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreEqualInAStructure(APIView):
    """
    Retrouvez les articles en stock inférieure ou égale à une valeur d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        articlestores = []
        for article_store in article_stores:
            if article_store.product.unit_pricing == request.value:
                articlestores.__add__(article_store)
        serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(serializer.data)

class ListOfArticleStoreCountInAStructure(APIView):
    """
    Retrouvez le nombre d'articles en stock d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.count()
        # articlestores = []
        # for article_store in article_stores:
        #     if article_store.product.unit_pricing == request.value:
        #         articlestores.__add__(article_store)
        # serializer = ArticleStoreSerializer(articlestores, many=True, context={'request': request})
        return Response(articlestores)

class ListOfArticleStoreValueInAStructure(APIView):
    """
    Retrouvez la valeur machande des articles en stock d'une structure
    """
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, id):
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        article_stores = (self.get_object(id)).article_stores.all()
        total = 0
        for article_store in article_stores:
            total += article_store.product.unit_pricing * article_store.theoric_stock
        return Response(total)