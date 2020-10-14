import random
import string
import uuid
import datetime
import math
from PIL import Image
from django.db import models
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext as _
from gocom.models import BusinessTransaction
from company.models import Structure
from product.models import Product
from django.utils.crypto import get_random_string
# Create your models here.


YES = 1
NO = 0
VALUE_CHOICES = [
    (YES, 'Yes'),
    (NO, 'No'),
]

ENTREE = 1
SORTIE = 0
MOVEMENT_CHOICES = [
    (ENTREE, 'In'),
    (SORTIE, 'Out'),
]

DRAFT = 0#'Draft'
PENDING = 1#'Pending'
CANCELLED = 3#'Cancelled'
SUCCEEDED = 2#'Succeeded'
STATUS_CHOICES = [
    (DRAFT, 'Draft'),
    (PENDING, 'Pending'),
    (CANCELLED, 'Canceled'),
    (SUCCEEDED, 'Succeeded'),
]


class InventoryMotif(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code = 'INV_MOT_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    code = models.CharField(max_length=30, default=generate_code, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="inventorymotifs",
        verbose_name="Structure associée"
    )

    class Meta:
        verbose_name_plural = "Motifs d'inventaire"
        ordering = ['created_at']

class InventoryType(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code = 'INV_TYP_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    code = models.CharField(max_length=30, default=generate_code, unique=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="inventorytypes",
        verbose_name="Structure associée"
    )

    class Meta:
        verbose_name_plural = "Types d'inventaire"
        ordering = ['created_at']

class SourceMovement(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code = 'MOV_SRC_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    code = models.CharField(max_length=30, default=generate_code, unique=True)
    wording = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    apply_as_input = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )
    output_application = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )

    sequence_number = models.PositiveIntegerField(null=True)

    #business_transaction = models.PositiveIntegerField(null=True)

    business_transaction = models.ForeignKey(
        'gocom.BusinessTransaction',
        null=True, 
        on_delete=models.PROTECT,
        related_name="source_movements",
        verbose_name="Transaction associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="source_movements",
        verbose_name="Structure associée"
    )

    class Meta:
        verbose_name_plural = "Source du mouvement"
        ordering = ['created_at']

class ArticleStore(models.Model):

    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = 'ART_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    def isAvailable(self):
        return (self.replenishment_level < self.theoric_stock)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')

    reference = models.CharField(max_length=255,null=True, default= generate_code)
    stock_max = models.PositiveIntegerField(null=True)
    stock_min = models.PositiveIntegerField(null=True)
    replenishment_level = models.PositiveIntegerField(null=True)
    unavailable = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )
    physical_stock = models.PositiveIntegerField(null=True)
    theoric_stock = models.PositiveIntegerField(null=True)
    cumulative_entry = models.PositiveIntegerField(null=True, default=1)
    cumulative_output = models.PositiveIntegerField(null=True, default=1)

    manufactury_date = models.DateField(auto_now_add=True,  verbose_name="Date de fabrication")
    expiry_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date d'expiration")
    last_inventory_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de dernier inventaire")
    
    #product = models.PositiveIntegerField(null=True)

    #structure = models.PositiveIntegerField(null=True)

    product = models.ForeignKey(
        'product.Product', 
        null=True,
        on_delete=models.PROTECT,
        related_name="article_stores",
        verbose_name="Produit associé"
    )
    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="article_stores",
        verbose_name="Structure associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Articles en Stock"
        ordering = ['created_at']

    def __str__(self):
        return "Article ["+self.reference+ "]: "


class StockMovement(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = 'MOV_STCK_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    def generate_code_object():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = 'OBJ_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    def generate_code_movement():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = 'MOV_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    def default_exercise():
        thedate = datetime.datetime.now()
        thelastyeardate = datetime.datetime.now() - datetime.timedelta(days=1*365)

        exercice = '%s/%s'% (thelastyeardate.year, thedate.year)
        return exercice

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    code_ref = models.CharField(max_length=30, default=generate_code, unique=True)
    object_ref = models.CharField(max_length=30, default=generate_code_object, unique=True)
    movement_object_ref = models.CharField(max_length=30, default=generate_code_movement, unique=True)

    label = models.CharField(max_length=255, null=True)
    notes = models.TextField(max_length=255, null=True)

    movement_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de mouvement")
    last_inventory_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de dernier inventaire")
    
    exercice = models.CharField(max_length=255, null=True, default=default_exercise)

    #store = models.PositiveIntegerField(null=True)

    #structure = models.PositiveIntegerField(null=True)

    source_movement = models.ForeignKey(
        'SourceMovement', 
        on_delete=models.PROTECT,
        related_name="stock_movements",
        verbose_name="Source du mouvement associée"
    )

    initiator = models.ForeignKey('auth.User', related_name='stock_movement_initiator', on_delete=models.PROTECT)

    # exercice = models.ForeignKey(
    #     'Excercice', 
    #     on_delete=models.PROTECT,
    #     verbose_name="Excercice associé"
    # )
    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="stock_movements",
        verbose_name="Structure associée"
    )
    # store = models.ForeignKey(
    #     'Store', 
    #     on_delete=models.PROTECT,
    #     verbose_name="Magasin associé"
    # )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Mouvement de Stock"
        ordering = ['created_at']


class MovementDetail(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')

    movement_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de mouvement")

    entree = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )

    sortie = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )

    sens_movement = models.PositiveIntegerField(
        choices=MOVEMENT_CHOICES,
        default=ENTREE,
    )

    quantity_moved = models.PositiveIntegerField(null=True)

    pre_movement_balance = models.IntegerField(null=True)

    stock_movement = models.ForeignKey(
        'StockMovement', 
        on_delete=models.PROTECT,
        related_name="movement_details",
        verbose_name="Mouvement de stock associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        related_name="movement_details",
        verbose_name="Article associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Détails d'un mouvement pour un article"
        ordering = ['created_at']

    @transaction.atomic
    def save(self, *args, **kwargs):
        article_store = self.article_store
        with transaction.atomic():
            self.pre_movement_balance = article_store.theoric_stock
            if self.sens_movement == 1:
                article_store.theoric_stock+= self.quantity_moved
                article_store.save()
            if self.sens_movement == 0:
                article_store.theoric_stock-= self.quantity_moved
                article_store.save()
class Inventory(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = 'INV_'+'%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    code = models.CharField(max_length=30, default=generate_code, unique=True)

    fox = models.CharField(max_length=15, blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    
    open_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date d'ouverture inventaire")
    end_date = models.DateTimeField(verbose_name="Date de fermeture inventaire")
    validation_date = models.DateTimeField(verbose_name="Date de validation inventaire")

    validation_state = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    user = models.ForeignKey('auth.User', related_name='inventory_initiator', on_delete=models.PROTECT)

    inventory_type = models.ForeignKey(
        'InventoryType', 
        on_delete=models.PROTECT,
        related_name="inventories",
        verbose_name="Type inventaire associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        related_name="inventories",
        verbose_name="Article associé"
    )

    inventory_motif = models.ForeignKey(
        'InventoryMotif', 
        on_delete=models.PROTECT,
        related_name="inventories",
        verbose_name="Motif inventaire associé"
    )

    structure = models.ForeignKey(
        'company.Structure', 
        null=True,
        on_delete=models.PROTECT,
        related_name="inventories",
        verbose_name="Structure associée"
    )


    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Inventaires"
        ordering = ['created_at']

class InventoryDetail(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    
    old_stock_quantity = models.PositiveIntegerField(null=True, verbose_name='Ancienne quantité')
    new_stock_quantity = models.PositiveIntegerField(null=True, verbose_name='Nouvelle quantité')

    gap = models.IntegerField(null=True, verbose_name='Ecart')

    inventory = models.ForeignKey(
        'Inventory', 
        on_delete=models.PROTECT,
        related_name="inventorie_details",
        verbose_name="Inventaire associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        related_name="inventorie_details",
        verbose_name="Article associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Détails d'inventaire pour un article en stock"
        ordering = ['created_at']