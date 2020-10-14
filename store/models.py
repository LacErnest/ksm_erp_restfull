import random
import string
import uuid
import datetime
import math
from PIL import Image
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
# Create your models here.


YES = 1
NO = 0
VALUE_CHOICES = [
    (YES, 'Yes'),
    (NO, 'No'),
]

ENTREE = 'In'
SORTIE = 'Out'
MOVEMENT_CHOICES = [
    (ENTREE, 'In'),
    (SORTIE, 'Out'),
]

DRAFT = 'Draft'
PENDING = 'Pending'
CANCELLED = 'Cancelled'
SUCCEEDED = 'Succeeded'
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
        code = '%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    inventory_motif_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=15, default=generate_code, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

class InventoryType(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code = '%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    inventory_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=15, default=generate_code, unique=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

class SourceMovement(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code = '%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code

    source_movement_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=15, default=generate_code, unique=True)
    wording = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    apply_as_input = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )
    output_application = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )

    sequence_number = models.PositiveIntegerField(null=True)

    business_transaction = models.PositiveIntegerField(null=True)

    '''business_transaction = models.ForeignKey(
        'BusinessTransaction', 
        on_delete=models.PROTECT,
        verbose_name="Transaction associée"
    )'''

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")


class ArticleStore(models.Model):

    article_store_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    stock_max = models.PositiveIntegerField(null=True)
    stock_min = models.PositiveIntegerField(null=True)
    replenishment_level = models.PositiveIntegerField(null=True)
    unavailable = models.PositiveIntegerField(
        choices=VALUE_CHOICES,
        default=NO,
    )
    physical_stock = models.PositiveIntegerField(null=True)
    theoric_stock = models.PositiveIntegerField(null=True)
    cumulative_entry = models.PositiveIntegerField(null=True)
    cumulative_output = models.PositiveIntegerField(null=True)

    manufactury_date = models.DateField(auto_now_add=True,  verbose_name="Date de fabrication")
    expiry_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date d'expiration")
    last_inventory_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de dernier inventaire")
    
    product = models.PositiveIntegerField(null=True)

    structure = models.PositiveIntegerField(null=True)

    '''product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        verbose_name="Produit associé"
    )
    structure = models.ForeignKey(
        'Structure', 
        on_delete=models.PROTECT,
        verbose_name="Structure associée"
    )'''

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")


class StockMovement(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = '%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    stock_movement_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_ref = models.CharField(max_length=15, default=generate_code, unique=True)
    object_ref = models.CharField(max_length=15, default=generate_code, unique=True)
    movement_object_ref = models.CharField(max_length=15, default=generate_code, unique=True)

    label = models.CharField(max_length=255, null=True)
    notes = models.CharField(max_length=255, null=True)

    movement_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date d'expiration")
    last_inventory_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date de dernier inventaire")

    stock_movement_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    exercice = models.PositiveIntegerField(null=True)

    store = models.PositiveIntegerField(null=True)

    structure = models.PositiveIntegerField(null=True)

    source_movement = models.ForeignKey(
        'SourceMovement', 
        on_delete=models.PROTECT,
        verbose_name="Source du mouvement associée"
    )

    user = models.ForeignKey('auth.User', related_name='store_stock_movement', on_delete=models.PROTECT)

    '''exercice = models.ForeignKey(
        'Excercice', 
        on_delete=models.PROTECT,
        verbose_name="Excercice associé"
    )
    structure = models.ForeignKey(
        'Structure', 
        on_delete=models.PROTECT,
        verbose_name="Structure associée"
    )
    store = models.ForeignKey(
        'Store', 
        on_delete=models.PROTECT,
        verbose_name="Magasin associé"
    )'''

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")


class MovementDetail(models.Model):

    movement_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
        verbose_name="Mouvement de stock associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        verbose_name="Article associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

class Inventory(models.Model):
    def generate_code():
        uid = get_random_string(length=5, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        thedate = datetime.datetime.now()
        code_ref = '%s%s%s%s' % (thedate.year, thedate.month, thedate.day, uid)
        return code_ref

    code = models.CharField(max_length=15, default=generate_code, unique=True)

    inventory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    open_date = models.DateTimeField(auto_now_add=True,  verbose_name="Date d'ouverture inventaire")
    end_date = models.DateTimeField(verbose_name="Date de fermeture inventaire")
    validation_date = models.DateTimeField(verbose_name="Date de validation inventaire")

    validation_state = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    fox = models.PositiveIntegerField(null=True)

    inventory_type = models.ForeignKey(
        'InventoryType', 
        on_delete=models.PROTECT,
        verbose_name="Type inventaire associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        verbose_name="Article associé"
    )

    inventory_motif = models.ForeignKey(
        'InventoryMotif', 
        on_delete=models.PROTECT,
        verbose_name="Motif inventaire associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")



class InventoryDetail(models.Model):

    inventory_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    old_stock_quantity = models.PositiveIntegerField(null=True)
    new_stock_quantity = models.PositiveIntegerField(null=True)

    gap = models.IntegerField(null=True)

    inventory = models.ForeignKey(
        'Inventory', 
        on_delete=models.PROTECT,
        verbose_name="Inventaire associé"
    )

    article_store = models.ForeignKey(
        'ArticleStore', 
        on_delete=models.PROTECT,
        verbose_name="Article associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")