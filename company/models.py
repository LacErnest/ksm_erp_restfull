from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from company.validators import *
import datetime
import uuid
from phone_field import PhoneField

# Create your models here.

# Définition de notre classe Company, précisement un model
class Company(models.Model): 
    """Model définissant une entreprise caractérisée par :
    - son nom (attribut: name (CharField: max_length=100, unique=True))
    - sa date de fondation (attribut: founding_date (DateField()))
    - son site web (attribut: web_site (URLField))
    - l'adresse de son QG (attribut: head_office_address (CharField: max_length=150))
    - sa messagerie électronique principale  (attribut: mail_address_one (EmailField: max_length=100))
    - sa messagerie électronique secondaire (attribut: mail_address_two (EmailField: max_length=100)))
    - son numéro de téléphone principal  (attribut: telephone_one (PhoneField: max_length=100)))
    - son numéro de téléphone secondaire  (attribut: telephone_two (PhoneField: max_length=100)))
    - son secteur économique (attribut: economic_sphere (CharField: choices=TYPE_ECONOMIC_SPHERE_CHOICES, max_length=50))
    - son chiffre d'affaires (attribut: sales_turnover (DecimalField: max_digits=22, decimal_places=2)))
    - son nombre d'employés (attribut: number_of_employees (PositiveIntegerField: max_digits=10))
    - son classement selon sa taille et son impact économique (attribut: sizing_and_economic_impact (CharField: choices=TYPE_SIZING_AND_ECONOMIC_IMPACT_CHOICES, max_length=50))
    - son secteur d'activité (attribut: business_sector (CharField: max_length=100))
    - sa branche d'activité  (attribut: business_line (CharField: max_length=100 ))
    - son forme juridique (attribut: legal_form (CharField: choices=TYPE_LEGAL_FORM_CHOICES, max_length=100 ))
    - son objet social (attribut: company_s_object (CharField: choices=TYPE_COMPANY_S_OBJECT_CHOICES, max_length=100 ))
    - la description de sa mission (attribut: mission (TextField: max_length=300 ))
    - son histoire (attribut: history (TextField: max_length=300 ))
    - sa description (attribut: description (description: max_length=300 ))"""

    TYPE_ECONOMIC_SPHERE_CHOICES = (
        ('RESOURCE_INDUSTRY','RESOURCE INDUSTRY'),
        ('MANUFACTURING_INDUSTRY','MANUFACTURING INDUSTRY'),
        ('SERVICE_SECTOR','SERVICE SECTOR'),
    )

    TYPE_SIZING_AND_ECONOMIC_IMPACT_CHOICES = (
        ('MICRO_COMPANY','MICRO-COMPANY'),
        ('VERY_SMALL_COMPANY','VERY SMALL COMPANY'),
        ('SMALL_BUSINESS','SMALL BUSINESS'),
        ('MEDIUM_SIZED_COMPANY','MEDIUM-SIZED COMPANY'),
        ('BIG_COMPANY','BIG COMPANY'),
        ('COMPANY_GROUP','COMPANY GROUP'),
        ('EXTENTED_COMPANY','EXTENTED COMPANY'),
    )  

    TYPE_LEGAL_FORM_CHOICES = (
        ('INDIVIDUAL_COMPANY','INDIVIDUAL COMPANY'),
        ('CIVILIAN_SOCIETY','CIVILIAN SOCIETY'),
        ('TRADING_COMPANY','TRADING COMPANY'),
        ('ECONOMIC_INTEREST_GROUPING','ECONOMIC INTEREST GROUPING'),
        ('ASSOCIATION','ASSOCIATION'),
        ('COOPERATIVE_COMPANY','COOPERATIVE COMPANY'),
        ('MUTUAL_COMPANY','MUTUAL COMPANY'),
    )

    TYPE_COMPANY_S_OBJECT_CHOICES = (
        ('PRIVATE_FOR_PROFIT_COMPANY','PRIVATE FOR-PROFIT COMPANY'),
        ('PRIVATE_NON_PROFIT_COMPANY','PRIVATE NON-PROFIT COMPANY'),
        ('PUBLIC_SERVICE_COMPANY','PUBLIC SERVICE COMPANY'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='companies', on_delete=models.PROTECT, verbose_name="Utilisateur")

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    founding_date = models.DateField(verbose_name="Date de fondation")
    slug = models.SlugField(max_length=100)
    web_site = models.URLField(verbose_name="Site web", null=True)
    head_office_address = models.CharField(max_length=150, verbose_name="Adresse du siège social")
    mail_address_one = models.EmailField(max_length=100, unique=True, null=True, verbose_name="Messagerie électronique principale")
    mail_address_two = models.EmailField(max_length=100, unique=True, null=True, verbose_name="Messagerie électronique secondaire")
    telephone_one = PhoneField(max_length=20, unique=True, verbose_name="N° téléphone principale")
    telephone_two = PhoneField(max_length=20, unique=True, null=True, verbose_name="N° téléphone secondaire")
    economic_sphere = models.CharField(choices=TYPE_ECONOMIC_SPHERE_CHOICES, max_length=50, verbose_name="Secteur économique")
    sales_turnover = models.DecimalField(max_digits=22, decimal_places=2, null=True, verbose_name="Chiffre d'affaire")
    number_of_employees = models.PositiveIntegerField(verbose_name="Nombre d'employé", default=0)
    sizing_and_economic_impact = models.CharField(choices=TYPE_SIZING_AND_ECONOMIC_IMPACT_CHOICES, max_length=50, verbose_name="Taille et impact économique")
    business_sector = models.CharField(max_length=100, null=True, verbose_name="Secteur d'activité")
    business_line = models.CharField(max_length=100, null=True, verbose_name="Branche d'activité")
    legal_form = models.CharField(choices=TYPE_LEGAL_FORM_CHOICES, max_length=100, verbose_name="Forme juridique")
    company_s_object = models.CharField(choices=TYPE_COMPANY_S_OBJECT_CHOICES, max_length=100, verbose_name="Objet social")
    mission = models.TextField(max_length=300, null=True, verbose_name="Mission")
    history = models.TextField(max_length=300, null=True, verbose_name="Histoire")
    description = models.TextField(max_length=300, null=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Entreprises" 
        ordering = ['created_at']

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        entreprises que nous traiterons plus tard
        """
        return self.name

# Définition de notre classe Structure, précisement un model
class Structure(models.Model): 
    """Model définissant une structure caractérisée par :
    - son nom (attribut: name (CharField: max_length=100, unique=True))
    - son site web (attribut: web_site (URLField))
    - son adresse (attribut: adresse (CharField: max_length=100))
    - sa messagerie electronique (attribut: mail_address (EmailField: max_length=100))
    - sa forme juridique (attribut: legal_form (CharField: max_length=100 ))
    - le type de structure (attribut: type_structure (CharField: choices=TYPE_STRUCTURE_CHOICES, max_length=50))
    - la latitude de sa localisation  (attribut: latitude (DecimalField: max_digits=14, decimal_places=2))
    - la longitude de sa localisation  (attribut: longitude (DecimalField: max_digits=14, decimal_places=2))
    - le nom de ville de sa localisation  (attribut: town_name (CharField: max_length=100 ))
    - le nom du pays de sa localisation (attribut: country_name (CharField: max_length=50 ))
    - le nom du continent de sa localisation (attribut: mainland_name (CharField: max_length=10 ))
    - sa description (attribut: description (TextField: max_length=200))
    - la référence de la compagnie à laquelle la structure  est associé (attribut: encompassing_structure (ForeignKey: 'Structure'))
    - la référence de la structure qui l'englobe, si elle existe (attribut: immediate_superior_structure (ForeignKey: 'Structure', null=True))"""

    TYPE_STRUCTURE_CHOICES = (
        ('STORE','STORE'),
        ('SELLING_POINT','SELLING POINT'),
        ('AGENCY','AGENCY'),
        ('HEAD_QUATER','HEAD QUATER'),
        ('SUBSIDIARY_COMPANY','SUBSIDIARY COMPANY')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_structures', on_delete=models.PROTECT, verbose_name="Utilisateur")

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100)
    web_site = models.URLField(verbose_name="Site web", null=True)
    adresse = models.CharField(max_length=100, verbose_name="Adresse")
    legal_position = models.CharField(max_length=100, verbose_name="Situation juridique", null=True)
    type_structure = models.CharField(choices=TYPE_STRUCTURE_CHOICES, max_length=50, verbose_name="Type de structure")
    latitude = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Longitude")
    town_name = models.CharField(max_length=100, verbose_name="Nom de la ville")
    country_name = models.CharField(max_length=50, verbose_name="Nom du pays")
    mainland_name = models.CharField(max_length=10, verbose_name="Nom du continent")
    description = models.TextField(max_length=200, verbose_name="Description", null=True)

    encompassing_structure = models.ForeignKey(
        'Company',
        related_name='structures',
        on_delete=models.PROTECT,
        verbose_name="Compagnie  associée"
    )
    direct_top_structure = models.ForeignKey(
        'Structure',
        null=True, 
        related_name='directly_lower_structures',
        on_delete=models.PROTECT,
        verbose_name="Structure directement supérieure"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Structures" 
        ordering = ['created_at']

    def __str__(self):
        """ 
        Cette méthode nous permettra de reconnaître facilement les différentes 
        structures que nous traiterons plus tard
        """
        return self.name

# Définition de notre classe Service, précisement un model
class Service(models.Model): 
    """Model définissant un poste caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son libellé (attribut: label (CharField: max_length=100))
    - sa mission (attribut: mission (TextField: max_length=200))
    - sa description (attribut: description (TextField: max_length=200))
    - son nombre d'equipement (attribut: count_equipment (PositiveIntegerField))
    - le nombre d'employé dans ce service (attribut: number_employee (PositiveIntegerField))
    - la structure à laquelle le service est associé (attribut: structure (ForeignKey: 'Structure'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_services', on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100)
    label = models.CharField(max_length=100, unique=True, verbose_name="Libellé")
    mission = models.TextField(max_length=200, verbose_name="Mission")
    description = models.TextField(max_length=200, verbose_name="Description")
    number_employee = models.PositiveIntegerField(verbose_name="Nombre d'employé dans ce service", default=0)
    count_equipment = models.PositiveIntegerField(verbose_name="Nombre d'équipements", default=0)
    structure = models.ForeignKey(
        'Structure',
        related_name='services',
        on_delete=models.PROTECT,
        verbose_name="Structure associée"
    )
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Services"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        services que nous traiterons plus tard
        """
        return self.code

# Définition de notre classe EquipmentType, précisement un model
class EquipmentType(models.Model): 
    """Model définissant un type d'équipement caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son libellé (attribut: label (CharField: max_length=100))
    - le  nombre de ce type d'équipement (attribut: count_type (PositiveIntegerField))
    - sa description (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_equiment_types', on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100) 
    label = models.CharField(max_length=100, verbose_name="Libellé")
    count_type = models.PositiveIntegerField(verbose_name="Nombre de ce type d'équipement", default=0)
    description = models.TextField(max_length=200, verbose_name="Description")
    services = models.ManyToManyField('Service', through='Equipment', related_name="equipment_types")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Type d'équipements"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        type d'équipement que nous traiterons plus tard
        """
        return self.code

# Définition de notre classe Equipment, précisement un model      
class Equipment(models.Model): 
    """Model définissant un équipement caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son libellé (attribut: label (CharField: max_length=100))
    - sa date d'acquisition (attribut: vesting_date (DateField))
    - sa date d'expiration (attribut: expiry_date (DateField))
    - sa description (attribut: description (TextField: max_length=200))
    - le type d'équipement (attribut: equipment_type (ForeignKey: EquipmentType))
    - son service (attribut: service (OneToOneField: Service))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_equipements', on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100) 
    label = models.CharField(max_length=100, verbose_name="Libellé")
    vesting_date = models.DateField(verbose_name="Date d'acquisition")
    expiry_date = models.DateField(verbose_name="Date d'expiration")
    description = models.TextField(max_length=200, verbose_name="Description")

    equipment_type = models.ForeignKey(
        'EquipmentType',
        related_name='equipments',
        on_delete=models.PROTECT,
        verbose_name="Type d'équipement associé"
    )
    service = models.ForeignKey(
        'Service',
        related_name='equipments',
        on_delete=models.PROTECT,
        verbose_name="Service associé"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Type d'équipement"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        type d'équipement que nous traiterons plus tard
        """
        return self.code

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer une equipement dans un service dans la BD"""
        with transaction.atomic():
            try:
                equipement_previous = Equipment.objects.get(id=self.id) 
                if  self.equipment_type is not equipement_previous.equipment_type:
                    equipement_previous.equipment_type.count_type -= 1
                    equipement_previous.equipment_type.save()
                    self.equipment_type.count_type += 1
                    self.equipment_type.save()
                if self.service is not equipement_previous.service:
                    equipement_previous.service.count_equipment -= 1
                    equipement_previous.service.save()
                    self.service.count_equipment += 1
                    self.service.save()   
            except Equipment.DoesNotExist:
                self.equipment_type.count_type += 1
                self.equipment_type.save()
                self.service.count_equipment += 1
                self.service.save()
            super(Equipment, self).save(*args, **kwargs)

# Définition de notre classe CompanyPartnerType, précisement un model
class CompanyPartnerType(models.Model): 
    """Model définissant un type de patenaire caractérisé par:
    - son code (attribut: code (CharField: max_length=50))
    - son libellé (attribut: label (CharField: max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_partner_types', on_delete=models.PROTECT)

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

    @classmethod
    def create(cls, partner_type):
        """
        Cette méthode nous permettra de creer un type de partenariat
        """
        company_partner_type = cls.objects.create( 
            id=partner_type.id, 
            user=partner_type.user,
            slug=partner_type.slug,
            code=partner_type.code, 
            label=partner_type.label, 
            description=partner_type.description
        )
        return company_partner_type

    def update(self, partner_type):
        """
        Cette méthode nous permettra de mettre à jour un type de partenariat
        """
        self.slug = partner_type.slug, 
        self.code = partner_type.code, 
        self.label = partner_type.label, 
        self.description = partner_type.description
        self.save()
    
# Définition de notre classe CompanyPartner, précisement un model
class CompanyPartner(models.Model): 
    """Model définissant un partenaire  par:
    - son nom (attribut: name (CharField: max_length=100))
    - son état (attribut: state (CharField: max_length=50, null=True))
    - sa photo (attribut: photo (ImageField: upload_to="photos/"))
    - sa raison sociale (attribut: social_reason (CharField: max_length=100, null=True))
    - sa situation juridique  (attribut: juridical_form (CharField: max_length=100, null=True))
    - sa societé (attribut: society (CharField: max_length=100, null=True))
    - sa description (attribut: description (TextField: max_length=200))
    - sa famille (attribut: family (CharField: max_length=100))
    - sa ville (attribut: city (CharField,  max_length=50))
    - son pays (attribut: country (CharField: max_length=50))
    - sa date de fondation (attribut: founding_date (DateTimeField))
    - la référence de son adresse par defaut (attribut: patner_adress_default (ForeignKey: 'PartnerAdresse'))
    - son type de partenariat (attribut: partner_type (CharField: max_length=100))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_partners', on_delete=models.PROTECT)

    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    state = models.CharField(max_length=50, null=True, verbose_name="Statut")
    photo = models.ImageField(upload_to="photos/", verbose_name="Photo / Logo")
    social_reason = models.CharField(max_length=100, null=True, verbose_name="Raison sociale")
    juridical_form = models.CharField(max_length=100, null=True, verbose_name="Forme juridique")
    society = models.CharField(max_length=100, null=True, verbose_name="Entreprise")
    description = models.TextField(max_length=200, verbose_name="Description du partenariat")
    family = models.CharField(max_length=100, null=True, verbose_name="Famille")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, verbose_name="Pays")
    creation_date = models.DateField(verbose_name="Date de naissance / création")
    partner_type = models.ForeignKey('CompanyPartnerType',  on_delete=models.PROTECT, verbose_name="Type de partenariat associé",  related_name="partners")
    structures = models.ManyToManyField('Structure', through='Contract', related_name="partners")

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
        return "{0}, type partenaire : {1}".format(self.name, self.partner_type)

    @classmethod
    def create(cls, partner):
        """
        Cette méthode nous permettra de creer un partenaire
        """
        company_partner = cls.objects.create( 
            id=partner.id,
            user=partner.user,
            name=partner.name,
            slug=partner.slug,
            matricule=partner.matricule,
            state=partner.state,
            photo=partner.photo,
            social_reason=partner.social_reason,
            juridical_form=partner.juridical_form,
            society=partner.society,
            description=partner.description,
            family=partner.family,
            city=partner.city,
            country=partner.country,
            creation_date=partner.creation_date,
            partner_type=CompanyPartnerType.objects.get(id=partner.partner_type.id)
        )
        return company_partner

    def update(self, partner):
        """
        Cette méthode nous permettra de mettre à jour un partenaire
        """
        self.name = partner.name 
        self.slug = partner.slug
        self.matricule = partner.matricule
        self.state = partner.state
        self.photo = partner.photo
        self.social_reason = partner.social_reason
        self.juridical_form = partner.juridical_form
        self.society = partner.society
        self.description = partner.description
        self.family = partner.family
        self.city = partner.city
        self.country = partner.country
        self.creation_date = partner.creation_date
        self.partner_type = CompanyPartnerType.objects.get(id=partner.partner_type.id)
        self.save()

# Définition de notre classe Function, précisement un model
class Function(models.Model): 
    """Model définissant un type d'équipement caractérisé par:
    - son libellé (attribut: label (CharField: max_length=100))
    - le nombre d'employé occupant cette fonction (attribut: number_employee (PositiveIntegerField))
    - sa description (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_functions', on_delete=models.PROTECT)

    label = models.CharField(max_length=100, unique=True, verbose_name="Libellé")
    slug = models.SlugField(max_length=100) 
    description = models.TextField(max_length=200, verbose_name="Description")
    number_employee = models.PositiveIntegerField(verbose_name="Nombre d'employé sous cette fonction", default=0)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Fonctions"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        fonctions que nous traiterons plus tard
        """
        return self.label

# Définition de notre classe Employee, précisement un model
class Employee(models.Model): 
    """Model définissant un employé caractérisé par:
    - son matricule (attribut: matricule (CharField: max_length=100))
    - son nom (attribut: name (CharField: max_length=100))
    - son prénom (attribut: surname (CharField: max_length=100))
    - sa date de naissance (attribut: birth_date (DateField))
    - son lieu de naissance (attribut: birth_place (CharField: max_length=100))
    - sa nationalité (attribut: nationality (CharField: max_length=100))
    - son sexe (attribut: sex (CharField: choices=SEXE_CHOICES, max_length=100))
    - son numéro CNI (attribut: no_cni (CharField: max_length=100))
    - son adresse électronique (attribut: mail_address (EmailField: max_length=100))
    - son téléphone (attribut: phone (PhoneField))
    - son CV (attribut: curriculum_vitae (FileField))
    - la référence de son grade (attribut: grade (ForeignKey: 'Grade'))
    - la référence de son indice (attribut: index (ForeignKey: 'Index'))
    - la référence de son servive (attribut: service (ForeignKey: 'Service'))
    - la référence de sa fonction (attribut: function (ForeignKey: 'Function'))"""
    
    SEXE_CHOICES = (
        ('MALE','MALE'),
        ('FEMALE','FEMALE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_employees', on_delete=models.PROTECT)

    matricule = models.CharField(max_length=100, unique=True, verbose_name="Matricule")
    name = models.CharField(max_length=100, verbose_name="Nom")
    surname = models.CharField(max_length=100, verbose_name="Prénom")
    slug = models.SlugField(max_length=100) 
    birth_date = models.DateField(verbose_name="Date de naissance")
    birth_place = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    nationality = models.CharField(max_length=100, verbose_name="Nationalité")
    sex = models.CharField(choices=SEXE_CHOICES, max_length=10, verbose_name="Sexe")
    no_cni = models.CharField(max_length=20, verbose_name="N° CNI")
    mail_address = models.EmailField(max_length=100, verbose_name="Adresse électronique")
    phone = models.CharField(max_length=20, verbose_name="N° téléphone")
    curriculum_vitae = models.FileField(verbose_name="Curriculum vitae")
    structure = models.ManyToManyField('Structure', through='Contract', related_name="employees")

    grade = models.ForeignKey(
        'Grade',
        related_name="employees",
        on_delete=models.PROTECT,
        verbose_name="Grade concerné"
    )
    index = models.ForeignKey(
        'Index',
        related_name="employees",
        on_delete=models.PROTECT,
        verbose_name="Indice concernée"
    )
    service = models.ForeignKey(
        'Service',
        related_name="employees",
        on_delete=models.PROTECT,
        verbose_name="Service concerné"
    )
    function = models.ForeignKey(
        'Function',
        related_name="employees",
        on_delete=models.PROTECT,
        verbose_name="Fonction concernée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Employés"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        employés que nous traiterons plus tard
        """
        return self.matricule

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer un employé dans la BD"""
        with transaction.atomic():
            try:
                employee_previous = Employee.objects.get(id=self.id) 
                promotion = Promotion.objects.order_by('-promotion_date').filter(employee=employee_previous)
                if promotion.exists():
                    promotion = promotion.first()
                    if  self.grade is not employee_previous.grade:
                        employee_previous.grade.number_employee -= 1
                        employee_previous.grade.save()
                        self.grade.number_employee += 1
                        self.grade.save()
                        promotion.grade = self.grade
                        promotion.save()
                    if self.index is not employee_previous.index:
                        employee_previous.index.number_employee -= 1
                        employee_previous.index.save()
                        self.index.number_employee += 1
                        self.index.save() 
                        promotion.index = self.index
                        promotion.save()
                    if self.service is not employee_previous.service:
                        employee_previous.service.number_employee -= 1
                        self.service.structure.encompassing_structure.number_employee -= 1
                        self.service.structure.encompassing_structure.save()
                        employee_previous.service.save()
                        self.service.number_employee += 1
                        self.service.save() 
                        promotion.service = self.service
                        promotion.save()
                    if self.function is not employee_previous.function:
                        employee_previous.function.number_employee -= 1
                        employee_previous.function.save()
                        self.function.number_employee += 1
                        self.function.save()
                    print("upadte employyee")
                super(Employee, self).save(*args, **kwargs)  
            except Employee.DoesNotExist:
                self.index.number_employee += 1
                self.index.save()
                self.grade.number_employee += 1
                self.grade.save()
                self.service.number_employee += 1
                self.service.structure.encompassing_structure.number_employee += 1
                self.service.structure.encompassing_structure.save()
                self.service.save()
                self.function.number_employee += 1
                self.function.save()
                super(Employee, self).save(*args, **kwargs) 
                employee = Employee.objects.get(id=self.id) 
                Promotion.objects.create(user=self.user, employee=employee, grade=self.grade, index=self.index, service=self.service, function=self.function)          

# Définition de notre classe Contract, précisement un model
class Contract(models.Model): 
    """Model définissant le contrat d'un(e) employé(e) caractérisé par:
    - sa date d'écriture (attribut: entry_date (DateField))
    - sa date de signature (attribut: signing_date (DateField))
    - sa date de début (attribut: start_date (DateField))
    - sa date de fin (attribut: end_date (DateField))   
    - son type de contrat (type_contract: name (CharField: choices=CONTRACT_CHOICES, max_length=50))
    - sa renouvelabilité (attribut: renewable (CharField: choices=RENEWABLE_CHOICES, max_length=50))
    - son statut (attribut: state (CharField: choices=STATE_CHOICES, max_length=50))
    - sa description  (attribut: description (TextField: max_length=200))
    - ses document (attribut: document (FileField))
    - la référence de l'employé(e) s'il s'agit d'un(e) employé(e) (attribut: employee (ForeignKey: 'Employee'))
    - la référence du partenaire, s'il s'agit d'un(e) partenaire (attribut: partner (ForeignKey: 'Partner'))"""

    CONTRACT_CHOICES = (
        ('EMPLOYEE','EMPLOYEE'),
        ('PARTNER','PARTNER')
    )

    RENEWABLE_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    STATE_CHOICES = (
        ('IN_PROGRESS','IN PROGRESS'),
        ('SUSPENDED','SUSPENDED'),
        ('CLOSED','CLOSED')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_contracts', on_delete=models.PROTECT)

    entry_date = models.DateField(verbose_name="Date d'écriture")
    signing_date = models.DateField(verbose_name="Date de la signature")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date d'expiration")
    type_contract = models.CharField(choices=CONTRACT_CHOICES, max_length=50, verbose_name="Choix du contrat")
    renewable = models.CharField(choices=RENEWABLE_CHOICES, max_length=50, verbose_name="Renouvelable")
    state = models.CharField(choices=STATE_CHOICES, max_length=50, verbose_name="Statut")
    structure = models.ForeignKey(
        'Structure',  
        on_delete=models.PROTECT,
        related_name="contracts", 
        verbose_name="Structure concernée"
    )
    employee = models.ForeignKey(
        'Employee', 
        null=True,
        related_name="contracts",
        on_delete=models.PROTECT,
        verbose_name="Employé(e) si concerné(e)"
    )
    partner =  models.ForeignKey(
        'CompanyPartner', 
        null=True,
        related_name="contracts",
        on_delete=models.PROTECT,
        verbose_name="Partenaire si concerné(e)"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de la dernière modification")
    
    class Meta:
        verbose_name_plural = "Contrats"
        ordering = ['created_at']
        unique_together = ('structure', 'employe')
        unique_together = ('structure', 'partner')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        contrats que nous traiterons plus tard
        """
        return "{0} de {1}".format(self.type_contract, ((self.partner, self.employee)[self.employee]))

# Définition de notre classe Responsability, précisement un model
class Responsability(models.Model): 
    """Model définissant une responsabilté caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son libellé (attribut: label (CharField: max_length=100))
    - sa prime en pourcentage ou non (attribut: percentage_bonus (CharField: choices=RESPONSABILITY_BONUS_CHOICES, max_length=50))
    - sa valeur en pourcentage ou en montant (attribut: value_amount_or_percentage (DecimalField: max_digits=6,  decimal_places=2))
    - sa description (attribut: description (TextField: max_length=200))"""

    def validate_value_amount_or_percentage(self):
        pass

    RESPONSABILITY_BONUS_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_responsabilities', on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100) 
    label = models.CharField(max_length=100, verbose_name="Libellé", unique=True)
    percentage_bonus = models.CharField(choices=RESPONSABILITY_BONUS_CHOICES, max_length=50, verbose_name="Prime en pourcentage")
    value_amount_or_percentage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur du montant/pourcentage")
    description = models.TextField(max_length=200, verbose_name="Description")
    employees = models.ManyToManyField('Employee', through='EmployeeResponsability', related_name="responsabilities")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Responsabilités"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        responsabilités que nous traiterons plus tard
        """
        return self.code

# Définition de notre classe EmployeeResponsability, précisement un model
class EmployeeResponsability(models.Model): 
    """Model définissant la responsabilité d'un employé caractérisé par:
    - son statut (attribut: label (CharField: choices=STATE_CHOICES, max_length=100))
    - sa date d'acquisition (attribut: grant_date (DateField))
    - sa date de suspension (attribut: suspension_date (DateField))
    - sa description (attribut: description (TextField: max_length=200))
    - la référence  de l'employé (attribut: employee (TextField: max_length=200))
    - la référence de la structure (attribut: responsability (TextField: max_length=200))"""

    STATE_CHOICES = (
        ('IN_PROGRESS','IN PROGRESS'),
        ('SUSPENDED','SUSPENDED'),
        ('CLOSED','CLOSED')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_employee_responsabilities', on_delete=models.PROTECT)

    state = models.CharField(choices=STATE_CHOICES, max_length=50, verbose_name="Statut")
    slug = models.SlugField(max_length=100) 
    grant_date = models.DateField(verbose_name="Date d'attribution")
    suspension_date = models.DateField(verbose_name="Date de suspension", null=True)

    employee = models.ForeignKey(
        'Employee', 
        related_name="employee_responsabilities",
        on_delete=models.PROTECT,
        verbose_name="Employé(e) concerné(e)"
    )
    responsability =  models.ForeignKey(
        'Responsability', 
        related_name="employee_responsabilities",
        on_delete=models.PROTECT,
        verbose_name="Responsabilité concerné"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Responsabilités des employés"
        ordering = ['created_at']
        unique_together = ('employee', 'responsability')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les responsabilités 
        des employés que nous traiterons plus tard
        """
        return "{0} de {1}".format(self.responsability, self.employee)

# Définition de notre classe Restraint, précisement un model
class Restraint(models.Model): 
    """Model définissant une responsabilté caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son libellé (attribut: label (CharField: max_length=100))
    - sa prime en pourcentage ou non (attribut: percentage_bonus (CharField: choices=RESPONSABILITY_BONUS_CHOICES, max_length=50))
    - sa valeur en pourcentage ou en montant (attribut: value_amount_or_percentage (DecimalField: max_digits=6,  decimal_places=2))"""

    def validate_value_amount_or_percentage(self):
        pass
    PERCENTAGE_DEDUCTION_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_restraints', on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    slug = models.SlugField(max_length=100) 
    label = models.CharField(max_length=100, verbose_name="Libellé")
    percentage_deduction = models.CharField(choices=PERCENTAGE_DEDUCTION_CHOICES, max_length=50,  verbose_name="Retenue en pourcentage")
    value_amount_or_percentage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur du montant/pourcentage")
    description = models.TextField(max_length=200, verbose_name="Description")
    employees = models.ManyToManyField('Employee', through='EmployeeRestraint', related_name="restrains")

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Eléments de retenue"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        éléments de retenue que nous traiterons plus tard
        """
        return self.code

# Définition de notre classe EmployeeRestraint, précisement un model
class EmployeeRestraint(models.Model): 
    """Model définissant un élément de retenue d'un employé caractérisé par:
    - son statut (attribut: label (CharField: choices=STATE_CHOICES, max_length=100))
    - sa date de soumission (attribut: submission_date (DateField))
    - sa date de suspension (attribut: suspension_date (DateField))
    - la réference  de l'employé (attribut: employee (TextField: max_length=200))
    - la réference de l'élément de retenue (attribut: responsability (TextField: max_length=200))"""

    STATE_CHOICES = (
        ('IN_PROGRESS','IN PROGRESS'),
        ('SUSPENDED','SUSPENDED'),
        ('CLOSED','CLOSED')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_employee_restraints', on_delete=models.PROTECT)

    state = models.CharField(choices=STATE_CHOICES, max_length=50, verbose_name="Statut")
    slug = models.SlugField(max_length=100) 
    submission_date = models.DateField(verbose_name="Date de soumission")
    suspension_date = models.DateField(verbose_name="Date de suspension", null=True)
    description = models.TextField(max_length=200, verbose_name="Description")

    employee = models.ForeignKey(
        'Employee', 
        related_name="employee_restraints",
        on_delete=models.PROTECT,
        verbose_name="Employé(e) concerné(e)"
    )
    restraint =  models.ForeignKey(
        'Restraint', 
        related_name="employee_restraints",
        on_delete=models.PROTECT,
        verbose_name="Elément de retenue concerné"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Responsabilités des employés"
        ordering = ['created_at']
        unique_together = ('employee', 'restraint')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les éléments de retenue 
        des employés que nous traiterons plus tard
        """
        return "{0} de {1}".format(self.restraint, self.employee)

# Définition de notre classe Grade, précisement un model
class Grade(models.Model): 
    """Model définissant un type d'équipement caractérisé par:
    - son code (attribut: code (CharField: max_length=100))
    - son label (attribut: libellé (CharField: max_length=100))
    - sa description (attribut: description (TextField: max_length=200))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_grades', on_delete=models.PROTECT)

    label = models.CharField(max_length=100, verbose_name="Libellé", unique=True)
    slug = models.SlugField(max_length=100) 
    description = models.TextField(max_length=200, verbose_name="Description")
    number_employee = models.PositiveIntegerField(verbose_name="Nombre d'employé sous ce grade", default=0)
    next_higher_grade = models.ForeignKey(
        'Grade', 
        null=True,
        related_name="next_lower_grades",
        on_delete=models.PROTECT,
        verbose_name="Grade directement supérieur"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Grades"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différents 
        grades que nous traiterons plus tard
        """
        return self.label

# Définition de notre classe Index, précisement un model
class Index(models.Model): 
    """Model définissant l'indice d'un grade caractérisé par:
    - sa valeur (attribut: value (DecimalField: max_digits=6, decimal_places=2))
    - la référence de son grade (attribut: grade (ForeignKey: 'Grade'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_indexes', on_delete=models.PROTECT)
    
    value = models.DecimalField(max_digits=6, unique=True, decimal_places=2, verbose_name="Valeur")
    slug = models.SlugField(max_length=100) 
    number_employee = models.PositiveIntegerField(verbose_name="Nombre d'employé sous cet indice", default=0)
    grade = models.ForeignKey(
        'Grade', 
        related_name="indexes",
        on_delete=models.PROTECT,
        verbose_name="Grade concerné"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Indices"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les différentes 
        indices que nous traiterons plus tard
        """
        return "{0}-{1}".format(self.grade, self.value)

# Définition de notre classe BasicSalary, précisement un model
class BasicSalary(models.Model): 
    """Model définissant le salaire de base en fonction du grade et de l'indice caractérisé par:
    - son montant (attribut: amount (DecimalField: max_digits=22, decimal_places=2))
    - la référence du grade (attribut: grade (ForeignKey: 'Grade'))
    - la référence de l'indice (attribut: index (ForeignKey: 'Index'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_basic_salaries', on_delete=models.PROTECT)
    
    amount = models.DecimalField(max_digits=22, decimal_places=2, verbose_name="Montant")
    slug = models.SlugField(max_length=100) 
    grade = models.ForeignKey(
        'Grade', 
        related_name="basic_salaries",
        on_delete=models.PROTECT,
        verbose_name="Grade concerné"
    )
    index = models.ForeignKey(
        'Index', 
        related_name="basic_salaries",
        on_delete=models.PROTECT,
        verbose_name="Indice concernée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Salaires de base"
        ordering = ['created_at']
        unique_together = ('grade', 'index')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les  
        salaires de base que nous traiterons plus tard
        """
        return "{0} de {1}".format(self.grade, self.index)

# Définition de notre classe StaffSalary, précisement un model
class StaffSalary(models.Model): 
    """Model définissant le salaire d'un employé caractérisé par:
    - son montant cumulé des primes (attribut: premium_accrual (DecimalField: max_digits=22, decimal_places=2))
    - son montant cumulé des déductions (attribut: accumulated_deductions (DecimalField: max_digits=22, decimal_places=2))
    - son montant à verser (attribut: amount_due (DecimalField: max_digits=22, decimal_places=2))
    - la référence de l'employé (attribut: grade (ForeignKey: 'Grade'))
    - la référence du salaire de base (attribut: index (ForeignKey: 'Index'))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_staff_salaries', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=100) 
    
    premium_accrual = models.DecimalField(max_digits=22, decimal_places=2, verbose_name="Montant cumulé des primes")
    accumulated_deductions = models.DecimalField(max_digits=22, decimal_places=2, verbose_name="Montant cumulé des déductions")
    amount_due = models.DecimalField(max_digits=22, decimal_places=2, verbose_name="Montant à verser")

    employee = models.ForeignKey(
        'Employee', 
        related_name="staff_salaries",
        on_delete=models.PROTECT,
        verbose_name="Employé(e) concerné(e)"
    )
    basic_salary = models.ForeignKey(
        'BasicSalary', 
        related_name="staff_salaries",
        on_delete=models.PROTECT,
        verbose_name="Salaire de base concerné"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Salaires de base"
        ordering = ['created_at']

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les  
        salaires des employés que nous traiterons plus tard
        """
        return "{0} de {1}".format(self.employee, self.basic_salary)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer le salaire d'un employé dans la BD"""
        with transaction.atomic():
            if not self.accumulated_deductions:
                self.calculation_of_deductions()
            if not self.premium_accrual:
                self.calculation_of_premiums()
            self.amount_due = self.basic_salary.amount + self.premium_accrual - self.accumulated_deductions
            super(StaffSalary, self).save(*args, **kwargs)
    
    def calculation_of_deductions(self):
        for employee_restraint in self.employee.employee_restraints.all():
            if employee_restraint.state == 'IN PROGRESS':
                if employee_restraint.restrain.percentage_deduction == 'YES':
                    self.accumulated_deductions += (employee_restraint.restrain.value_amount_or_percentage * self.basic_salary.amount) / 100 
                else:
                    self.accumulated_deductions += employee_restraint.restrain.value_amount_or_percentage 

    def calculation_of_premiums(self):
        for employee_responsability in self.employee.employee_responsabilities.all():
            if employee_responsability.state == 'IN PROGRESS':
                if employee_responsability.responsability.percentage_bonus == 'YES':
                    self.premium_accrual += (employee_responsability.responsability.value_amount_or_percentage * self.basic_salary.amount) / 100 
                else:
                    self.premium_accrual += employee_responsability.responsability.value_amount_or_percentage 

# Définition de notre classe Promotion, précisement un model
class Promotion(models.Model): 
    """Model définissant la promotion d'un employé caractérisé par:
    - la référence de son grade (attribut: premium_accrual (ForeignKey: 'Grade'))
    - la référence de son indice (attribut: accumulated_deductions (ForeignKey: 'Index'))
    - la référence de l'employé (attribut: grade (ForeignKey: 'Employee'))
    - la date de promotion (attribut: promotion_date (DateField))"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    user = models.ForeignKey('auth.User', related_name='company_promotions', on_delete=models.PROTECT)
    
    promotion_date = models.DateField(auto_now_add=True, verbose_name="Date de la promotion")
    slug = models.SlugField(max_length=100) 
    employee = models.ForeignKey(
        'Employee', 
        related_name="promotions",
        on_delete=models.PROTECT,
        verbose_name="Employé(e) concerné(e)"
    )
    grade = models.ForeignKey(
        'Grade', 
        related_name="promotions",
        on_delete=models.PROTECT,
        verbose_name="Grade concerné"
    )
    index = models.ForeignKey(
        'Index', 
        related_name="promotions",
        on_delete=models.PROTECT,
        verbose_name="Indice concerné"
    )
    service = models.ForeignKey(
        'Service',
        related_name="promotions",
        on_delete=models.PROTECT,
        verbose_name="Service concerné"
    )
    function = models.ForeignKey(
        'Function',
        related_name="promotions",
        on_delete=models.PROTECT,
        verbose_name="Fonction concernée"
    )

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    
    class Meta:
        verbose_name_plural = "Salaires de base"
        ordering = ['created_at']
        unique_together = ('employee', 'grade', 'index', 'service', 'function', 'created_at')

    def __str__(self):
        """
        Cette méthode nous permettra de reconnaître facilement les  
        salaires des employés que nous traiterons plus tard
        """
        return "{0}-{1}-{2}".format(self.employee, self.grade, self.index)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Cette méthode nous permet d'enregistrer une promotion dans la BD"""
        with transaction.atomic():
            try:
                promotion_previous = Promotion.objects.get(id=self.id) 
                print("upadte promotion")
                super(Promotion, self).save(*args, **kwargs) 
            except Promotion.DoesNotExist:
                super(Promotion, self).save(*args, **kwargs) 
                self.employee.grade = self.grade
                self.employee.index = self.index
                self.employee.service = self.service
                self.employee.function = self.function
                self.employee.save()