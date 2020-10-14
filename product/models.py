from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
import datetime
import uuid

# Create your models here.

# Définition de notre classe Language, précisement un model
class Language(models.Model): 
    """Model définissant une langue caractérisée par :
    - son code (attribut: code (CharField: max_length=6, unique=True ))
    - son nom (attribut: name (CharField: max_length=30 ))
    - une indication permettant de connaitre si c'est la langue par defaut (attribut: is_default (choices=IS_DEFAULT_CHOICES, max_length=6))"""

    def validate_is_default(value): 
        """Cette méthode nous permet de vérifier que la langue par defaut est unique"""
        if value == 'YES':
            language = Language.objects.filter(is_default='YES')
            if language.exists():
                raise ValidationError("There is already a default language")

    IS_DEFAULT_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_language', on_delete=models.PROTECT)
    
    code = models.CharField(max_length=6, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    is_default = models.CharField(choices=IS_DEFAULT_CHOICES, max_length=3, validators=[validate_is_default], verbose_name="Langue par défaut")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    products = models.ManyToManyField('Product', through='ProductDescription', related_name="languages")
    categories = models.ManyToManyField('Category', through='CategoryDescription', related_name="languages")
    
    class Meta:
        verbose_name_plural = "Langues"
        ordering = ['created_at']

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        langues que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.name, self.code)

# Définition de notre classe Categorie, précisement un model
class Category(models.Model): 
    """Model définissant une catégorie caractérisée par :
    - son code (attribut: code (CharField: max_length=30))
    - son nom (attribut: name (CharField: max_length=100))
    - son image (attribut: image (ImageField))
    - une indication permettant de connaitre si c'est la categorie racine ou non (attribut: root_category (CharField: choices=IS_DEFAULT_CHOICES,))
    - l'activation/desactivation, de la mise à jour de son code (attribut: update_code (CharField: choices=IS_DEFAULT_CHOICES,))
    - l'activation/desactivation, de la mise à jour des codes de ses produits  (attribut: update_code_product (CharField: choices=IS_DEFAULT_CHOICES,))
    - sa categorie parent, si elle existe (attribut: category_id (ForeignKey: 'Category', null=True.. ))"""

    def validate_code(value): 
        """Cette méthode nous permet de vérifier que le code ne contient pas d'espace"""
        if value.find(' ') != -1:
            print(repr(value.find(' ')))
            raise ValidationError("The code cannot contain spaces")

    def validate_name(value): 
        """Cette méthode nous permet de vérifier que le nom de la categorie est unique"""
        try:
            Category.objects.get(name=value.upper())
            raise ValidationError("this value must be unique")
        except Category.DoesNotExist:
            pass

    ROOT_CATEGORY_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )
    UPDATE_CODE_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )
    UPDATE_CODE_PRODUCT_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_categories', on_delete=models.PROTECT)

    code = models.CharField(max_length=6, unique=True, validators=[validate_code], verbose_name="Code", help_text="Personnaliser votre code, mais nous vous conseillons de nous laisser s'en charger")
<<<<<<< HEAD

=======
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom", validators=[validate_name])
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to="images/")
    update_code = models.CharField(choices=UPDATE_CODE_CHOICES,  max_length=6, help_text="Autoriser la mise à jour du code de la catégorie, lors d'un update", verbose_name="Mise à jour code")
    update_code_product = models.CharField(choices=UPDATE_CODE_PRODUCT_CHOICES, max_length=6, help_text="Autoriser la mise à jour du code des produits associés à cette catégorie, lors d'un update", verbose_name="Mise à jour code produits")
    category_parent = models.ForeignKey(
        'Category', 
        null=True,
        related_name='subcategories',
        on_delete=models.PROTECT,
        verbose_name="Catégorie Parente"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Catégories"
        ordering = ['created_at']

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        catégories que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.name, self.code)
        

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer une categorie dans la BD"""
        category = Category.objects.filter(id=self.id)  
        category_previous = None
        if category.exists():
            category_previous = category.first()
        # On initialise une transaction 
        with transaction.atomic():
            # Creation de la catégorie racine 
            if not Category.objects.filter(name='ROOT CATEGORY').exists() and self.name != "ROOT CATEGORY":
                root_category = Category.objects.create(
                    name = "ROOT CATEGORY", 
                    image = "images/téléchargement_4.jpg",
                    user=self.user,
                    code="ROO001",
                    update_code = "NO", 
                    update_code_product = "NO"
                )
                root_category.category_parent = root_category 
                root_category.save()
            if self.category_parent is None and self.name != "ROOT CATEGORY":
                self.category_parent = Category.objects.get(name="ROOT CATEGORY")
            self.generate_code(category)
            super(Category, self).save(*args, **kwargs)
            if self.update_code_product == "YES":
                if category_previous is not None:
                    if category_previous.name is not self.name:
                        products = Product.objects.filter(category=category_previous)
                        for product in products:
                            product.code = None
                            product.update_code = self.update_code_product
                            product.save() # On met a jour le code des produits concernés par la mise a jour du nom de la catégorie

    def generate_code(self, category):
        """ 
        Cette méthode nous permettra de génerer automatiquement le code d'une catégorie qui renseigne sur la 
        sur la quantième catégorie créée globalement
        """
        self.name = self.name.upper()
        if category.exists():
            category = category.first()
            if self.update_code == "YES":
                if self.code is None:
                    code_retrieve = False
                    k=1
                    while not code_retrieve:
                        category_count = Category.objects.all().count() + k
                        #FORMATTAGE DU CODE EN FONCTION DU NOMBRE DE CATEGORIE
                        if category_count < 10:
                            category_count_str = '00' + str(category_count)
                        elif category_count < 100:
                            category_count_str = '0' + str(category_count)
                        else:
                            category_count_str = str(category_count)
                        tempon_code = self.name.replace(" ", "") # On retire les espaces dans la chaîne
                        tempon_code = tempon_code[0:3]
                        tempon_code = tempon_code.upper()
                        self.code = tempon_code + category_count_str
                        if not Category.objects.filter(code=self.code).exists():
                            code_retrieve = True
                            k += 1
        else:    
            if self.code is None:
                code_retrieve = False
                k=1
                while not code_retrieve:
                    category_count = Category.objects.all().count() + k
                    #FORMATTAGE DU CODE EN FONCTION DU NOMBRE DE CATEGORIE
                    if category_count < 10:
                        category_count_str = '00' + str(category_count)
                    elif category_count < 100:
                        category_count_str = '0' + str(category_count)
                    else:
                        category_count_str = str(category_count)

                    tempon_code = self.name .replace(" ", "") # On retire les espaces dans la chaîne
                    tempon_code = tempon_code[0:3]
                    tempon_code = tempon_code.upper()
                    self.code = tempon_code + category_count_str
                    if not Category.objects.filter(code=self.code).exists():
                        code_retrieve = True
                        k += 1
            
# Définition de notre classe CategoryDescription, précisement un model
class CategoryDescription(models.Model): 
    """Model définissant la description d'une categorie dans une langue caractérisée par :
    - sa description (attribut: description (CharField: max_length=100, unique=True))
    - sa spécification (attribut: specification (TextField: max_length=200))
    - la langue associée (attribut: language (ForeignKey: 'Language' ))
    - la catégorie associée (attribut: category (ForeignKey: 'Category'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_category_descriptions', on_delete=models.PROTECT)

    specification = models.CharField(max_length=100, unique=True, verbose_name="Spécification")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")
    language = models.ForeignKey(
        'Language', 
        on_delete=models.PROTECT,
        verbose_name="Langue associée"
    )
    category = models.ForeignKey(
        'Category', 
        related_name='category_descriptions',
        on_delete=models.CASCADE,
        verbose_name="Catégorie associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Description des catégories dans différentes langues"
        ordering = ['created_at']
        unique_together = ('language', 'category')

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        langues que nous traiterons plus tard
        """
        return self.specification

# Définition de notre classe Conditioning, précisement un model
class Conditioning(models.Model): 
    """Model définissant un conditionnement caractérisé par :
    - son nom (attribut: name (CharField: max_length=100))
    - sa description (attribut: description (TextField: max_length=200))
    - sa quantité (attribut: quantity (PositiveIntegerField))"""

    def validate_name(value): 
        """Cette méthode nous permet de vérifier que le nom du packaging est unique"""
        try:
            Conditioning.objects.get(name=value.upper())
            raise ValidationError("this value must be unique")
        except Conditioning.DoesNotExist:
            pass

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_packagings', on_delete=models.PROTECT)
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom", validators=[validate_name])
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    products = models.ManyToManyField('Product', through='ProductPackaging', related_name="conditionnings")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Packagings"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        pack que nous traiterons plus tard
        """
        return "{0}, quantity:{1}".format(self.name, self.quantity)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Conditioning, self).save(*args, **kwargs)

# Définition de notre classe ProductDescription, précisement un model
class ProductDescription(models.Model): 
    """Model définissant la description d'un produit dans une langue caractérisée par :
    - sa description (attribut: description (CharField: max_length=100, unique=True))
    - sa spécification (attribut: specification (TextField: max_length=200))
    - la langue associée (attribut: language (ForeignKey: 'Language' ))
    - la catégorie associée (attribut: category (ForeignKey: 'Category'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_product_descriptions', on_delete=models.PROTECT)

    specification = models.CharField(max_length=100, unique=True, verbose_name="Spécification")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")
    language = models.ForeignKey(
        'Language', 
        on_delete=models.PROTECT,
        verbose_name="Langue associée"
    )
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE,
        verbose_name="Produit associée",
        related_name="product_descriptions"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Descriptions des produits dans différentes langues"
        ordering = ['created_at']
        unique_together = ('language', 'product')

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        langues que nous traiterons plus tard
        """
        return self.specification

# Définition de notre classe Product, précisement un model
class Product(models.Model): 
    """Model définissant un produit caractérisé par :
    - son code (attribut: code (CharField: max_length=100))
    - son nom (attribut: name (CharField: max_length=100))
    - l'activation/desactivation, de la mise à jour de son code (attribut: update_code (CharField: choices=IS_DEFAULT_CHOICES))
    - sa description par défaut (attribut: default_description (ForeignKey: 'ProductDescription'))
    - son packaging à l'achat (attribut: conditioning_purchase (ForeignKey: 'Conditioning'))
    - son packaging à la vente (attribut: conditioning_sale (ForeignKey: 'Conditioning'))
    - sa catégorie (attribut: conditioning_sale (ForeignKey: 'Category'))"""
    
    def validate_code(value): 
        """Cette méthode nous permet de vérifier que le code ne contient pas d'espace"""
        if value.find(' ') != -1:
            raise ValidationError("The code cannot contain spaces")
    
    def validate_name(value): 
        """Cette méthode nous permet de vérifier que le nom du produit est unique"""
        try:
            Product.objects.get(name=value.upper())
            raise ValidationError("this value must be unique")
        except Product.DoesNotExist:
            pass

    IS_DEFAULT_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='products', on_delete=models.PROTECT)

    code = models.CharField(max_length=10, unique=True, verbose_name="Code", validators=[validate_code], help_text="Personnaliser votre code, mais nous vous conseillons de nous laisser s'en charger")
<<<<<<< HEAD

=======
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom", validators=[validate_name])
    update_code = models.CharField(choices=IS_DEFAULT_CHOICES, max_length=3, verbose_name="Autoriser la mise à jour du code du produit")
    slug = models.SlugField(max_length=100)

    category = models.ForeignKey(
        'Category', 
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Catégorie associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Produits"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        produit que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.name, self.code)

    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer un produit dans la BD"""
        self.generate_code()
        super(Product, self).save(*args, **kwargs)

    def generate_code(self):
        """ 
        Cette méthode nous permettra de génerer automatiquement le code d'un produit qui renseigne sur la 
        categorie du produit, sur le quantième produit cree globalement et sur le quantième produit de la catégorie
        """
        self.name = self.name.upper()
        product = Product.objects.filter(id=self.id)

        if not product.exists():
            if self.code is None:
                code_retrieve = False
                k=1
                while not code_retrieve:
                    category_product_count = Product.objects.filter(category=self.category).count() + k
                    if category_product_count < 10:
                        category_product_count_str = '000' + str(category_product_count)
                    elif category_product_count < 100:
                        category_product_count_str = '00' + str(category_product_count)
                    elif category_product_count < 1000:
                        category_product_count_str = '0' + str(category_product_count)
                    else:
                        category_product_count_str = str(category_product_count)
                    self.code = self.category.code + category_product_count_str 
                    if not Product.objects.filter(code=self.code).exists():
                        code_retrieve = True
                        k += 1
        else:
            product = product.first()
            if self.update_code == "YES":
                if self.code is None:
                    if self.category != product.category:
                        code_retrieve = False
                        k=1
                        while not code_retrieve:
                            category_product_count = Product.objects.filter(category=self.category).count() + k
                            if category_product_count < 10:
                                category_product_count_str = '000' + str(category_product_count)
                            elif category_product_count < 100:
                                category_product_count_str = '00' + str(category_product_count)
                            elif category_product_count < 1000:
                                category_product_count_str = '0' + str(category_product_count)
                            else:
                                category_product_count_str = str(category_product_count)
                            self.code = self.category.code + category_product_count_str 
                            if not Product.objects.filter(code=self.code).exists():
                                code_retrieve = True
                                k += 1 
                    else:
                        self.code = self.category.code + product.code[6:10]          

# Définition de notre classe Tax, précisement un model
class Tax(models.Model): 
    """Model définissant une taxe caractérisée par :
    - son nom (attribut: name (CharField: max_length=100))
    - sa valeur (attribut: value (DecimalField: max_digits=12, decimal_places=2 ))
    - sa description (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_taxes', on_delete=models.PROTECT)

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valeur")
    description = models.TextField(max_length=200, verbose_name="Description")

    products = models.ManyToManyField('Product', through='ProductTaxation', related_name="taxes")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Taxes"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        taxes que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.name, self.value)

# Définition de notre classe ProductTaxation, précisement un model
class ProductTaxation(models.Model): 
    """Model définissant les taxes auxquelles un produit est assujetti caractérisé par :
    - le produit associé (attribut: product (ForeignKey: 'Product'))
    - la taxe associée description (attribut: tax (ForeignKey: 'Tax'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_product_taxations', on_delete=models.PROTECT)

    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        verbose_name="Produit associée"
    )
    tax = models.ForeignKey(
        'Tax', 
        on_delete=models.PROTECT,
        verbose_name="Taxe associée"
    )
    
    slug = models.SlugField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Taxes de produits"
        ordering = ['created_at']
        unique_together = ('product', 'tax')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        taxe d'un produit que nous traiterons plus tard
        """
        return  "{0}-{1}".format(self.product, self.tax)

# Définition de notre classe ProductPackaging, précisement un model
class ProductPackaging(models.Model): 
    """Model définissant les packaging auxquelles un produit est assujetti caractérisé par :
    - le produit associé (attribut: product (ForeignKey: 'Product'))
    - le conditionnement associée  (attribut: conditioning (ForeignKey: 'Conditioning'))
    - le type de conditionnement   (attribut: type_packaging (CharField))"""

    TYPE_PACKAGING_CHOICES = (
        ('SALE','SALE'),
        ('PURCHASE','PURCHASE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_product_packagings', on_delete=models.PROTECT)

    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        verbose_name="Produit associée"
    )
    conditioning = models.ForeignKey(
        'Conditioning', 
        on_delete=models.PROTECT,
        verbose_name="Conditioning associée",
    )
    type_packaging = models.CharField(choices=TYPE_PACKAGING_CHOICES, max_length=10, verbose_name="Type de conditionnement")
    
    slug = models.SlugField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Packaging des produits"
        ordering = ['created_at']
        unique_together = ('product', 'conditioning', 'type_packaging')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        packagings d'un produit que nous traiterons plus tard
        """
        return  "{0}-{1}".format(self.product, self.conditioning)

# Définition de notre classe Pricing, précisement un model
class Pricing(models.Model): 
    """Model définissant les tarifs d'un produit caractérisé par :
    - son prix moyen (attribut: average_sale_price (DecimalField(max_digits=12, decimal_places=2))
    - son prix de revient (attribut: cost_price (DecimalField(max_digits=12, decimal_places=2))
    - son prix unitaire (attribut: unit_pricing (DecimalField(max_digits=12, decimal_places=2))
    - son pourcentage de dépenses (attribut: percentage_expence DecimalField(max_digits=12, decimal_places=2)))
    - son taux de marge en pourcentage (attribut: percentage_margin_rate (DecimalField(max_digits=12, decimal_places=2))
    - son pourcentage des taxes sur les marques (attribut: percentage_brand_taxes (DecimalField(max_digits=12, decimal_places=2))
    - son prix du demi-gros (attribut: half_wholesale_price (DecimalField(max_digits=12, decimal_places=2))
    - son prix de gros (attribut: wholesale_price DecimalField(max_digits=12, decimal_places=2))
    - son pourcentage prix demi-gros  (attribut: percentage_half_big_price (DecimalField(max_digits=12, decimal_places=2))
    - son pourcentage prix gros  (attribut: percentage_wholesale_price (DecimalField(max_digits=12, decimal_places=2))
    - son prix total cumulé (attribut: total_accumulated_price (DecimalField(max_digits=12, decimal_places=2))
    - son type de tarification (à l'acchat ou à lq vente) (attribut: type_pricing (CharField(choices=TYPE_PRICING_CHOICES, max_length=10)
    - son produit  associée (attribut: product (DecimalField(max_digits=12, decimal_places=2))"""

    TYPE_PRICING_CHOICES = (
        ('SALE','SALE'),
        ('PURCHASE','PURCHASE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_pricing', on_delete=models.PROTECT)

    average_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix moyen")
    slug = models.SlugField(max_length=100)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix de revient")
    unit_pricing = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix unitaire")  
    percentage_expence = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Pourcentage des dépenses(transport...)")
    percentage_margin_rate = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Taux de marge en pourcentage")
    percentage_brand_taxes = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Pourcentage des taxes sur les marques")
    half_wholesale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix du demi-gros")
    wholesale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix de gros")
    percentage_half_big_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Pourcentage prix demi-gros")
    percentage_wholesale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Pourcentage prix gros")
    total_accumulated_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix total cumulé")
    type_pricing = models.CharField(choices=TYPE_PRICING_CHOICES, max_length=10, verbose_name="Type de tarif")
    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        related_name="pricing",
        verbose_name="Produit associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Tarifs"
        ordering = ['created_at']
        unique_together = ('product', 'type_pricing')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        tarifs que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.type_pricing, self.average_price)

# Définition de notre classe ProductDetail, précisement un model
class ProductDetail(models.Model): 
    """Model définissant le detail d'un produit caractérisé par :
    - son modèle (attribut: model (CharField: max_length=100))
    - sa marque (attribut: mark (CharField: 'max_length=100'))
    - son poids (attribut: weight (DecimalField: max_digits=12, decimal_places=2))
    - sa conservation (attribut: conservation (TextField: max_length=200))
    - son origine (attribut: origin (CharField: max_length=50))
    - sa composition (attribut: composition (TextField: max_length=200))
    - le produit associée (attribut: product (ForeignKey: 'Tax'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_product_details', on_delete=models.PROTECT)

    model = models.CharField(max_length=100, verbose_name="Modèle")
    slug = models.SlugField(max_length=100) 
    mark = models.CharField(max_length=100, verbose_name="Marque") 
    weight = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Poids") 
    conservation = models.TextField(max_length=200, verbose_name="Conservation") 
    origin = models.CharField(max_length=50, verbose_name="Origine") 
    composition = models.TextField(max_length=200, verbose_name="Composition") 
    product = models.OneToOneField(
        'Product', 
        on_delete=models.PROTECT,
        related_name="product_detail",
        verbose_name="Produit associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Details de produits"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les details 
        de différents produit que nous traiterons plus tard
        """
        return self.model    

# Définition de notre classe ProductIllustration, précisement un model
class ProductIllustration(models.Model): 
    """Model définissant l'illustration d'un produit est caractérisé par :
    - son image (attribut: model (ImageField: upload_to="images/"))
    - sa video (attribut: mark (FileField: upload_to="videos/"))
    - le produit associée (attribut: product (ForeignKey: 'Product'))"""

    TYPE_ILLUSTRATION_CHOICES = (
        ('IMAGE','IMAGE'),
        ('VIDEO','VIDEO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='product_product_illustrations', on_delete=models.PROTECT)
  
    illustration = models.FileField(upload_to="illustrations/", verbose_name="Image/Vidéo")
    slug = models.SlugField(max_length=100) 
    type_illustration = models.CharField(choices=TYPE_ILLUSTRATION_CHOICES, default="IMAGE", max_length=10, verbose_name="Type de l'illustration")
    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        related_name="product_illustrations",
        verbose_name="Produit associée "
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Illustrations des produits"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        illustrations d'un produit que nous traiterons plus tard
        """
        return self.product
