from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from phone_field import PhoneField
import datetime
import uuid
from django.apps import apps

# Create your models here.

# Définition de notre classe PartnerType, précisement un model
class PartnerType(models.Model): 
    """Model définissant un type de patenaire caractérisé par:
    - son code (attribut: code (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_partner_types', on_delete=models.PROTECT)

    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    label = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Types de partenaire"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        types de partenaire que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.label, self.code)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Cette méthode nous permet d'enregistrer un type de partenariat dans la BD
        pour l'API PARTNER et pour l'API COMPANY si elle est intégrée.
        """
        with transaction.atomic():
            try:
                partner_type =  PartnerType.objects.get(id=self.id)
                if apps.is_installed('company'):
                    from company.models import CompanyPartnerType
                    try:
                        company_partner_type =  CompanyPartnerType.objects.get(id=self.id) 
                        company_partner_type.update(self)
                    except CompanyPartnerType.DoesNotExist:
                        CompanyPartnerType.create(self)
            except PartnerType.DoesNotExist:
                if apps.is_installed('company'):
                    from company.models import CompanyPartnerType
                    try:
                        company_partner_type =  CompanyPartnerType.objects.get(
                            models.Q(id=self.id) | 
                            models.Q(code=self.code) |
                            models.Q(label=self.label)
                        )
                        self.change_partnership_type(company_partner_type)
                    except CompanyPartnerType.DoesNotExist:
                        CompanyPartnerType.create(self)
            super(PartnerType, self).save(*args, **kwargs)

    def change_partnership_type(self, company_partner_type):
        """
        Cette méthode permet de modifier les informations d'un type de partenaire.
        """   
        self.id = company_partner_type.id
        self.code = company_partner_type.code
        self.label = company_partner_type.label
        self.description = company_partner_type.description

# Définition de notre classe TypeAdresse, précisement un model
class TypeAdresse(models.Model): 
    """Model définissant un type d'adresse caractérisé par:
    - son code (attribut: label (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_type_adresses', on_delete=models.PROTECT)

    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    label = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")

    partners = models.ManyToManyField('Partner', through='PartnerAdresse', related_name="type_adresses")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Types d'adresse"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        types de d'adresse que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.label, self.code)

# Définition de notre classe PartnerAdresse, précisement un model
class PartnerAdresse(models.Model): 
    """Model définissant l'adresse d'un partenaire caractérisé par:
    - la référence de son type d'adresse (attribut: type_adresse (ForeignKey: 'TypeAdresse'))
    - la référence de son partenaire (attribut: partner (ForeignKey: 'Partner'))
    - sa longitude (attribut: longitude (DecimalField: max_digits=14, decimal_places=2))
    - sa latitude  (attribut: latitude (DecimalField: max_digits=14, decimal_places=2))
    - sa definition comme addresse par defaut ou non  (attribut: default_delivery_address (CharField: max_length=200))"""

    def validate_is_default(value): 
        """Cette méthode nous permet de vérifier que la langue par defaut est unique"""
        if value == 'YES':
            partner_adresse = PartnerAdresse.objects.filter(default_delivery_address='YES')
            if partner_adresse.exists():
                raise ValidationError("There is already a default address")

    DEFAULT_DELIVERY_ADDRESS_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_partner_adresses', on_delete=models.PROTECT)

    type_adresse = models.ForeignKey(
        'TypeAdresse', 
        on_delete=models.PROTECT,
        verbose_name="Type d'adresse associé(e)",
        related_name="partner_adresse" 
    )
    partner = models.ForeignKey(
        'Partner', 
        on_delete=models.PROTECT,
        verbose_name="Partenaire associé(e)",
        related_name="partner_adresse" 
    )
    slug = models.SlugField(max_length=100)
    longitude = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Longitude")
    latitude = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Latitude")
    default_delivery_address = models.CharField(choices=DEFAULT_DELIVERY_ADDRESS_CHOICES, max_length=3, validators=[validate_is_default], verbose_name="Definir comme adresse par défaut")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Adresses de partenaires"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        adresses de partenaire de d'adresse que nous traiterons plus tard
        """
        return self.partner 

# Définition de notre classe Partner, précisement un model
class Partner(models.Model): 
    """Model définissant un partenaire  par:
    - son nom (attribut: name (CharField: max_length=100))
    - son matricule (attribut: matricule (CharField: max_length=50, null=True))
    - son état (attribut: state (CharField: max_length=50, null=True))
    - sa photo (attribut: photo (ImageField: upload_to="photos/"))
    - sa raison sociale (attribut: social_reason (CharField: max_length=100, null=True))
    - sa situation juridique  (attribut: juridical_form (CharField: max_length=100, null=True))
    - sa societé (attribut: society (CharField: max_length=100, null=True))
    - sa description (attribut: description (TextField: max_length=200))
    - sa famille (attribut: family (CharField: max_length=100))
    - sa ville (attribut: city (CharField,  max_length=50))
    - son pays (attribut: country (CharField: max_length=50))
    - sa date de création (attribut: creation_date (DateTimeField))
    - la reference de son adresse par defaut (attribut: patner_adress_default (ForeignKey: 'PartnerAdresse'))
    - son type de partenariat (attribut: partner_type (ForeignKey: 'PartnerType'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='partners', on_delete=models.PROTECT)

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    state = models.CharField(max_length=50, null=True, verbose_name="Statut")
    photo = models.ImageField(upload_to="photos/", verbose_name="Photo / Logo")
    social_reason = models.CharField(max_length=100, null=True, verbose_name="Raison sociale")
    juridical_form = models.CharField(max_length=100, null=True, verbose_name="Forme juridique")
    society = models.CharField(max_length=100, null=True, verbose_name="Entreprise")
    description = models.TextField(max_length=200, verbose_name="Description du partenariat")
    family = models.CharField(max_length=100, null=True, verbose_name="Famille")
    city = models.CharField(max_length=50, verbose_name="Ville")
    country = models.CharField(max_length=50, verbose_name="Pays")
    creation_date = models.DateField(verbose_name="Date de naissance / création")

    partner_type = models.ForeignKey(
        'PartnerType', 
        on_delete=models.PROTECT,
        verbose_name="Type de partenariat associé", 
        related_name="partners"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Partenaires"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        partenaires que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.name, self.matricule)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Cette méthode nous permet d'enregistrer un partenaire dans la BD
        pour l'API PARTNER et pour l'API COMPANY si elle est intégrée
        """
        with transaction.atomic():
            try:
                partner =  Partner.objects.get(id=self.id)
                if apps.is_installed('company'):
                    from company.models import CompanyPartner
                    try:
                        company_partner = CompanyPartner.objects.get(id=self.id) 
                        company_partner.update(self)
                    except CompanyPartner.DoesNotExist:
                        CompanyPartner.create(self)    
            except Partner.DoesNotExist:
                if apps.is_installed('company'):
                    from company.models import CompanyPartner
                    try:
                        company_partner =  CompanyPartner.objects.get(
                            models.Q(id=self.id) | 
                            models.Q(matricule=self.matricule)
                        )
                        self.change_partnership_type(company_partner)
                    except CompanyPartner.DoesNotExist:
                        company_partner= CompanyPartner.create(self)
            super(Partner, self).save(*args, **kwargs)

    def change_partnership_type(self, company_partner):
        """
        Cette méthode permet de modifier les informations d'un partenaire
        """   
        self.name = company_partner.name 
        self.slug = company_partner.slug
        self.matricule = company_partner.matricule
        self.state = company_partner.state
        self.photo = company_partner.photo
        self.social_reason = company_partner.social_reason
        self.juridical_form = company_partner.juridical_form
        self.society = company_partner.society
        self.description = company_partner.description
        self.family = company_partner.family
        self.city = company_partner.city
        self.country = company_partner.country
        self.creation_date = company_partner.creation_date
        self.partner_type = PartnerType.objects.get(id=company_partner.partner_type.id)

# Définition de notre classe Contact, précisement un model
class Contact(models.Model): 
    """Model définissant un contact d'un partenaire caractérisé par:
    - son nom (attribut: code (CharField: max_length=10))
    - son numero de telephone (attribut: label (CharField: max_length=50))
    - son email (attribut: label (CharField: max_length=50))
    - son fax (attribut: label (CharField: max_length=50))
    - son code postal (attribut: label (CharField: max_length=50))
    - son site web (attribut: label (CharField: max_length=50))
    - son identifiant watsapp (attribut: label (CharField: max_length=50))
    - la référence du partenaire associé à ce contact (attribut: description (TextField: max_length=200))"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_contacts', on_delete=models.PROTECT)

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100)
    telephone = PhoneField(verbose_name="N° Téléphone")
    email = models.CharField(max_length=50, verbose_name="Email")
    fax = models.CharField(max_length=50, null=True, verbose_name="Fax")
    postal_code = models.CharField(max_length=50, unique=True, null=True, verbose_name="Code postal")
    web_site = models.URLField(max_length=50, null=True, help_text="https://www.yoyobb.com", verbose_name="Site web")
    whatsapp_id = PhoneField(help_text="Obligatoire", verbose_name="N° Téléphone watsapp")
    partner = models.ForeignKey(
        'Partner', 
        on_delete=models.PROTECT,
        verbose_name="Partenaire associé", 
        related_name="contacts"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        contacts que nous traiterons plus tard
        """
        return self.name

# Définition de notre classe Price, précisement un model
class Price(models.Model): 
    """Model définissant un prix caractérisé par:
    - son code (attribut: label (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_prices', on_delete=models.PROTECT)

    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    label = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")

    partners = models.ManyToManyField('Partner', through='EligiblePrice', related_name="prices")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Prix"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        prix de partenaire que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.label, self.code)

# Définition de notre classe EligiblePrice, précisement un model
class EligiblePrice(models.Model): 
    """Model définissant un prix auquel un partenaire est éligible caractérisé par:
    - la référence du partenaire associé (attribut: partner (ForeignKey: 'Partner'))
    - la référence du prix associé  (attribut: price (ForeignKey: 'Price'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_eligible_prices', on_delete=models.PROTECT)

    partner = models.ForeignKey(
        'Partner', 
        on_delete=models.PROTECT,
        verbose_name="Partenaire associé"
    )
    slug = models.SlugField(max_length=100)
    price = models.ForeignKey(
        'Price', 
        on_delete=models.PROTECT,
        verbose_name="Prix associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Prix éligibles"
        ordering = ['created_at']
        unique_together = ('partner', 'price')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        prix de partenaire que nous traiterons plus tard
        """
        return "{0}, {1}".format(self.partner, self.price)

# Définition de notre classe ExemptTaxe, précisement un model
class ExemptTaxe(models.Model): 
    """Model définissant une taxe exempté à un partenaire caractérisé par:
    - la référence du partenaire associé (attribut: partner (ForeignKey: 'Partner'))
    - la référence de la taxe  associé  (attribut: tax (ForeignKey: 'Tax'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_exempt_taxes', on_delete=models.PROTECT)

    partner = models.ForeignKey(
        'Partner', 
        on_delete=models.PROTECT,
        verbose_name="Partenaire associé"
    )
    slug = models.SlugField(max_length=100)
    tax = models.ForeignKey(
        'PartnerTax', 
        on_delete=models.PROTECT,
        verbose_name="Taxe associée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Taxes exemptées"
        ordering = ['created_at']
        unique_together = ('partner', 'tax')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        taxes exemptées de partenaire que nous traiterons plus tard
        """
        return "{0}, {1}".format(self.partner, self.tax)

# Définition de notre classe Tax, précisement un model
class PartnerTax(models.Model): 
    """Model définissant une taxe caractérisé par:
    - son code (attribut: label (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_taxes', on_delete=models.PROTECT)

    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    label = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, verbose_name="Description")

    partners = models.ManyToManyField('Partner', through='ExemptTaxe', related_name="taxes")

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
        return "{0}: {1}".format(self.label, self.code)

# Définition de notre classe PaymentMethod, précisement un model
class PaymentMethod(models.Model): 
    """Model définissant un moyen de payement caractérisé par:
    - son code (attribut: label (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - son code (attribut: code (CharField: max_length=10))
    - son image (attribut: image (ImageField: upload_to="images/"))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_payment_methods', on_delete=models.PROTECT)

    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    label = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to="images/" , verbose_name="Image")
    description = models.TextField(max_length=200, verbose_name="Description")

    partners = models.ManyToManyField('Partner', through='PartnerPaymentMethod', related_name="payment_methods")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural = "Moyens de payement"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        moyens de payement que nous traiterons plus tard
        """
        return "{0}: {1}".format(self.label, self.code)

# Définition de notre classe PartnerPaymentMethod, précisement un model
class PartnerPaymentMethod(models.Model): 
    """Model définissant un moyen de payement d'un partenaire caractérisé par:
    - la référence du partenaire associé (attribut: partner (ForeignKey: 'Partner'))
    - la référence de moyen de payement  associé  (attribut: payment_method (ForeignKey: 'PaymentMethod'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='patner_partner_payment_methods', on_delete=models.PROTECT)

    partner = models.ForeignKey(
        'Partner', 
        on_delete=models.PROTECT,
        verbose_name="Partenaire associé",
    )
    slug = models.SlugField(max_length=100)
    payment_method = models.ForeignKey(
        'PaymentMethod', 
        on_delete=models.PROTECT,
        verbose_name="Moyen de payement associé"
    )

    value = models.CharField(max_length=100, verbose_name="N° Téléphone/ N° Compte")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name_plural="Moyens de payement des partenaires"
        ordering = ['created_at']
        unique_together = ('partner', 'payment_method')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        moyens de payement des partenaires que nous traiterons plus tard
        """
        return "{0}, {1}".format(self.partner, self.payment_method)

