from django.db import models
import uuid

# Create your models here.

# Définition de notre classe Currency, précisement un model
class Currency(models.Model): 
    """Model définissant une monnaie caractérisé par:
    - son code (attribut: code (CharField: max_length=10))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='gocom_currencies', on_delete=models.PROTECT)

    code = models.CharField(max_length=10)
    slug = models.SlugField(max_length=100)
    label = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Monnaies"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        monnaies que nous traiterons plus tard
        """
        return self.label

# Définition de notre classe BusinessTransactionOrigin , précisement un model
class BusinessTransactionOrigin(models.Model): 
    """Model définissant l'origine d'une transaction caractérisé par:
    - son type (attribut: type_business_transaction (CharField: choices=TYPE_BUSINESS_TRANSACTION_ORIGIN_CHOICES, max_length=30))
    - son application en entrée qui peut etre possible ou non (attribut: apply_as_input (CharField: choices=APPLY_AS_INPUT_CHOICES, max_length=6))
    - sa application en sortie qui peut etre possible ou non (attribut: output_application (CharField: choices=OUTPUT_APPLICATION_CHOICES, max_length=6))"""

    TYPE_BUSINESS_TRANSACTION_ORIGIN_CHOICES = (
        ('DEV','DEVIS'),
        ('FACT','FACTURE'),
        ('BDC','BON DE COMMANDE'),
        ('BDL','BON DE LIVRAISON')

    )
    APPLY_AS_INPUT_CHOICES = (
        ('OUI','OUI'),
        ('NON','NON')
    )
    OUTPUT_APPLICATION_CHOICES = (
        ('OUI','OUI'),
        ('NON','NON')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='gocom_business_transaction_origins', on_delete=models.PROTECT)

    type_business_transaction_origin = models.CharField(choices=TYPE_BUSINESS_TRANSACTION_ORIGIN_CHOICES, max_length=30)
    slug = models.SlugField(max_length=100)
    apply_as_input = models.CharField(choices=APPLY_AS_INPUT_CHOICES, max_length=6)
    output_application = models.CharField(choices=OUTPUT_APPLICATION_CHOICES, max_length=6)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Origines des transactions"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        origines de transaction que nous traiterons plus tard
        """
        return self.type_business_transaction_origin

# Définition de notre classe BusinessTransaction  , précisement un model
class BusinessTransaction(models.Model): 
    """Model définissant une transaction caractérisé par:
    - son type (attribut: type_business_transaction (CharField: choices=TYPE_BUSINESS_TRANSACTION_CHOICES, max_length=30))
    - sa remise globale (attribut: apply_as_input (DecimalField: max_digits=14, decimal_places=2))
    - son prix hors taxe (attribut: apply_as_input (DecimalField: max_digits=14, decimal_places=2))
    - sa TVA (attribut: apply_as_input (DecimalField: max_digits=5, decimal_places=2))
    - son impot sur les revenus (attribut: apply_as_input (DecimalField: max_digits=14, decimal_places=2))
    - son prix tous taxes comprises (attribut: apply_as_input (DecimalField: max_digits=14, decimal_places=2))
    - son prix net à payer (attribut: apply_as_input (DecimalField: max_digits=14, decimal_places=2))
    - la référence de la monnaie associée  (attribut: currency (ForeignKey: 'Currency'))
    - la référence de l'origine de la transaction (attribut: business_transaction_origin (ForeignKey: 'BusinessTransactionOrigin'))
    - la référence de la transaction antérieure si elle existe  (attribut: business_transaction (ForeignKey: 'BusinessTransaction'))
    - la référence du partenaire associée s'il existe  (attribut: patner (PositiveIntegerField))"""

    TYPE_BUSINESS_TRANSACTION_CHOICES = (
        ('PURCHASE','PURCHASE'),
        ('SALE','SALE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='gocom_business_transactions', on_delete=models.PROTECT)

    type_business_transaction = models.CharField(choices=TYPE_BUSINESS_TRANSACTION_CHOICES, max_length=20)
    slug = models.SlugField(max_length=100)
    overall_discount = models.DecimalField(max_digits=14, decimal_places=2)
    price_HT = models.DecimalField(max_digits=14, decimal_places=2)
    TVA = models.DecimalField(max_digits=5, decimal_places=2)
    IR = models.DecimalField(max_digits=14, decimal_places=2)
    price_TTC = models.DecimalField(max_digits=14, decimal_places=2)
    net_to_pay = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.PROTECT,
        verbose_name="Devises  de la transaction"
    )
    business_transaction_origin = models.ForeignKey(
        'BusinessTransactionOrigin',
        on_delete=models.PROTECT,
        verbose_name="Origine de la transaction associée"
    )
    business_transaction = models.ForeignKey(
        'BusinessTransaction',
        null=True,
        on_delete=models.PROTECT,
        verbose_name="La transaction anterieure liée si elle existe"
    )
    patner = models.PositiveIntegerField(verbose_name="Sa référence partenaire, s'il la transaction concerne un partenaire", null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        transactions que nous traiterons plus tard
        """
        return self.type_business_transaction

# Définition de notre classe BusinessTransactionDetail  , précisement un model
class BusinessTransactionDetail(models.Model): 
    """Model définissant les détails d'une transaction caractérisé par:
    - son prix à l'unité (attribut: unit_price (CharField: choices=TYPE_BUSINESS_TRANSACTION_CHOICES, max_length=30))
    - sa quantité (attribut: quantity (DecimalField: max_digits=14, decimal_places=2))
    - son remise (attribut: discount (DecimalField: max_digits=14, decimal_places=2))
    - son prix total (attribut: total_price (DecimalField: max_digits=14, decimal_places=22))
    - la référence de la transaction (attribut: business_transaction (ForeignKey: 'BusinessTransaction'))
    - la référence de l'article mouvementé et du magasin si la transaction conduit à un mouvement en stock (attribut: article_store (PositiveIntegerField))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='gocom_business_transaction_details', on_delete=models.PROTECT)
    
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    slug = models.SlugField(max_length=100)
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.DecimalField(max_digits=14, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)
    
    business_transaction = models.ForeignKey(
        'BusinessTransaction', 
        on_delete=models.PROTECT,
        verbose_name="La transaction anterieure liée si elle existe"
    )
    article_store = models.PositiveIntegerField(verbose_name="article et magasin concernée", null=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Détails des transactions"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        détails de transaction que nous traiterons plus tard
        """
        return self.business_transaction