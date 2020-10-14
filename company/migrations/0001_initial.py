# Generated by Django 3.0.7 on 2020-08-21 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicSalary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='Montant')),
                ('slug', models.SlugField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Salaires de base',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('founding_date', models.DateField(verbose_name='Date de fondation')),
                ('slug', models.SlugField(max_length=100)),
                ('web_site', models.URLField(verbose_name='Site web')),
                ('head_office_address', models.CharField(max_length=150, verbose_name='Adresse du siège social')),
                ('mail_address_one', models.EmailField(max_length=100, unique=True, verbose_name='Messagerie électronique principale')),
                ('mail_address_two', models.EmailField(max_length=100, unique=True, verbose_name='Messagerie électronique secondaire')),
                ('telephone_one', phone_field.models.PhoneField(max_length=20, unique=True, verbose_name='N° téléphone principale')),
                ('telephone_two', phone_field.models.PhoneField(max_length=20, unique=True, verbose_name='N° téléphone secondaire')),
                ('economic_sphere', models.CharField(choices=[('RESOURCE_INDUSTRY', 'RESOURCE INDUSTRY'), ('MANUFACTURING_INDUSTRY', 'MANUFACTURING INDUSTRY'), ('SERVICE_SECTOR', 'SERVICE SECTOR')], max_length=50, verbose_name='Secteur économique')),
                ('sales_turnover', models.DecimalField(decimal_places=2, max_digits=22, verbose_name="Chiffre d'affaire")),
                ('number_of_employees', models.PositiveIntegerField(default=0, verbose_name="Nombre d'employé")),
                ('sizing_and_economic_impact', models.CharField(choices=[('MICRO_COMPANY', 'MICRO-COMPANY'), ('VERY_SMALL_COMPANY', 'VERY SMALL COMPANY'), ('SMALL_BUSINESS', 'SMALL BUSINESS'), ('MEDIUM_SIZED_COMPANY', 'MEDIUM-SIZED COMPANY'), ('BIG_COMPANY', 'BIG COMPANY'), ('COMPANY_GROUP', 'COMPANY GROUP'), ('EXTENTED_COMPANY', 'EXTENTED COMPANY')], max_length=50, verbose_name='Taille et impact économique')),
                ('business_sector', models.CharField(max_length=100, verbose_name="Secteur d'activité")),
                ('business_line', models.CharField(max_length=100, verbose_name="Branche d'activité")),
                ('legal_form', models.CharField(choices=[('INDIVIDUAL_COMPANY', 'INDIVIDUAL COMPANY'), ('CIVILIAN_SOCIETY', 'CIVILIAN SOCIETY'), ('TRADING_COMPANY', 'TRADING COMPANY'), ('ECONOMIC_INTEREST_GROUPING', 'ECONOMIC INTEREST GROUPING'), ('ASSOCIATION', 'ASSOCIATION'), ('COOPERATIVE_COMPANY', 'COOPERATIVE COMPANY'), ('MUTUAL_COMPANY', 'MUTUAL COMPANY')], max_length=100, verbose_name='Forme juridique')),
                ('company_s_object', models.CharField(choices=[('PRIVATE_FOR_PROFIT_COMPANY', 'PRIVATE FOR-PROFIT COMPANY'), ('PRIVATE_NON_PROFIT_COMPANY', 'PRIVATE NON-PROFIT COMPANY'), ('PUBLIC_SERVICE_COMPANY', 'PUBLIC SERVICE COMPANY')], max_length=100, verbose_name='Objet social')),
                ('mission', models.TextField(max_length=300, verbose_name='Mission')),
                ('history', models.TextField(max_length=300, verbose_name='Histoire')),
                ('description', models.TextField(max_length=300, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='companies', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Entreprises',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CompanyPartner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=100)),
                ('matricule', models.CharField(max_length=50, unique=True, verbose_name='Matricule')),
                ('state', models.CharField(max_length=50, null=True, verbose_name='Statut')),
                ('photo', models.ImageField(upload_to='photos/', verbose_name='Photo / Logo')),
                ('social_reason', models.CharField(max_length=100, null=True, verbose_name='Raison sociale')),
                ('juridical_form', models.CharField(max_length=100, null=True, verbose_name='Forme juridique')),
                ('society', models.CharField(max_length=100, null=True, verbose_name='Entreprise')),
                ('description', models.TextField(max_length=200, verbose_name='Description du partenariat')),
                ('family', models.CharField(max_length=100, null=True, verbose_name='Famille')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('country', models.CharField(max_length=100, verbose_name='Pays')),
                ('creation_date', models.DateField(verbose_name='Date de naissance / création')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Partenaires',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(verbose_name="Date d'écriture")),
                ('signing_date', models.DateField(verbose_name='Date de la signature')),
                ('start_date', models.DateField(verbose_name='Date de début')),
                ('end_date', models.DateField(verbose_name="Date d'expiration")),
                ('type_contract', models.CharField(choices=[('EMPLOYEE', 'EMPLOYEE'), ('PARTNER', 'PARTNER')], max_length=50, verbose_name='Choix du contrat')),
                ('renewable', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=50, verbose_name='Renouvelable')),
                ('state', models.CharField(choices=[('IN_PROGRESS', 'IN PROGRESS'), ('SUSPENDED', 'SUSPENDED'), ('CLOSED', 'CLOSED')], max_length=50, verbose_name='Statut')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de la dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Contrats',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=100, unique=True, verbose_name='Matricule')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('surname', models.CharField(max_length=100, verbose_name='Prénom')),
                ('slug', models.SlugField(max_length=100)),
                ('birth_date', models.DateField(verbose_name='Date de naissance')),
                ('birth_place', models.CharField(max_length=100, verbose_name='Lieu de naissance')),
                ('nationality', models.CharField(max_length=100, verbose_name='Nationalité')),
                ('sex', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10, verbose_name='Sexe')),
                ('no_cni', models.CharField(max_length=20, verbose_name='N° CNI')),
                ('mail_address', models.EmailField(max_length=100, verbose_name='Adresse électronique')),
                ('phone', models.CharField(max_length=20, verbose_name='N° téléphone')),
                ('curriculum_vitae', models.FileField(upload_to='', verbose_name='Curriculum vitae')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Employés',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeResponsability',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('IN_PROGRESS', 'IN PROGRESS'), ('SUSPENDED', 'SUSPENDED'), ('CLOSED', 'CLOSED')], max_length=50, verbose_name='Statut')),
                ('slug', models.SlugField(max_length=100)),
                ('grant_date', models.DateField(verbose_name="Date d'attribution")),
                ('suspension_date', models.DateField(null=True, verbose_name='Date de suspension')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_responsabilities', to='company.Employee', verbose_name='Employé(e) concerné(e)')),
            ],
            options={
                'verbose_name_plural': 'Responsabilités des employés',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeRestraint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('IN_PROGRESS', 'IN PROGRESS'), ('SUSPENDED', 'SUSPENDED'), ('CLOSED', 'CLOSED')], max_length=50, verbose_name='Statut')),
                ('slug', models.SlugField(max_length=100)),
                ('submission_date', models.DateField(verbose_name='Date de soumission')),
                ('suspension_date', models.DateField(null=True, verbose_name='Date de suspension')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_restraints', to='company.Employee', verbose_name='Employé(e) concerné(e)')),
            ],
            options={
                'verbose_name_plural': 'Responsabilités des employés',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('slug', models.SlugField(max_length=100)),
                ('label', models.CharField(max_length=100, verbose_name='Libellé')),
                ('vesting_date', models.DateField(verbose_name="Date d'acquisition")),
                ('expiry_date', models.DateField(verbose_name="Date d'expiration")),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': "Type d'équipement",
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('number_employee', models.PositiveIntegerField(default=0, verbose_name="Nombre d'employé sous cette fonction")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_functions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Fonctions',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('number_employee', models.PositiveIntegerField(default=0, verbose_name="Nombre d'employé sous ce grade")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('next_higher_grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='next_lower_grades', to='company.Grade', verbose_name='Grade directement supérieur')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_grades', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Grades',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6, unique=True, verbose_name='Valeur')),
                ('slug', models.SlugField(max_length=100)),
                ('number_employee', models.PositiveIntegerField(default=0, verbose_name="Nombre d'employé sous cet indice")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='indexes', to='company.Grade', verbose_name='Grade concerné')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_indexes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Indices',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=100)),
                ('web_site', models.URLField(verbose_name='Site web')),
                ('adresse', models.CharField(max_length=100, verbose_name='Adresse')),
                ('legal_position', models.CharField(max_length=100, verbose_name='Situation juridique')),
                ('type_structure', models.CharField(choices=[('STORE', 'STORE'), ('SELLING_POINT', 'SELLING POINT'), ('AGENCY', 'AGENCY'), ('HEAD_QUATER', 'HEAD QUATER'), ('SUBSIDIARY_COMPANY', 'SUBSIDIARY COMPANY')], max_length=50, verbose_name='Type de structure')),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Longitude')),
                ('town_name', models.CharField(max_length=100, verbose_name='Nom de la ville')),
                ('country_name', models.CharField(max_length=50, verbose_name='Nom du pays')),
                ('mainland_name', models.CharField(max_length=10, verbose_name='Nom du continent')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('direct_top_structure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='directly_lower_structures', to='company.Structure', verbose_name='Structure directement supérieure')),
                ('encompassing_structure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='structures', to='company.Company', verbose_name='Compagnie  associée')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_structures', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Structures',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='StaffSalary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('premium_accrual', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='Montant cumulé des primes')),
                ('accumulated_deductions', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='Montant cumulé des déductions')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='Montant à verser')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('basic_salary', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='staff_salaries', to='company.BasicSalary', verbose_name='Salaire de base concerné')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='staff_salaries', to='company.Employee', verbose_name='Employé(e) concerné(e)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_staff_salaries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Salaires de base',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('slug', models.SlugField(max_length=100)),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='Libellé')),
                ('mission', models.TextField(max_length=200, verbose_name='Mission')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('number_employee', models.PositiveIntegerField(default=0, verbose_name="Nombre d'employé dans ce service")),
                ('count_equipment', models.PositiveIntegerField(default=0, verbose_name="Nombre d'équipements")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='company.Structure', verbose_name='Structure associée')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Services',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Restraint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('slug', models.SlugField(max_length=100)),
                ('label', models.CharField(max_length=100, verbose_name='Libellé')),
                ('percentage_deduction', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=50, verbose_name='Retenue en pourcentage')),
                ('value_amount_or_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valeur du montant/pourcentage')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('employees', models.ManyToManyField(related_name='restrains', through='company.EmployeeRestraint', to='company.Employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_restraints', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Eléments de retenue',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Responsability',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('slug', models.SlugField(max_length=100)),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='Libellé')),
                ('percentage_bonus', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=50, verbose_name='Prime en pourcentage')),
                ('value_amount_or_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valeur du montant/pourcentage')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('employees', models.ManyToManyField(related_name='responsabilities', through='company.EmployeeResponsability', to='company.Employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_responsabilities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Responsabilités',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('slug', models.SlugField(max_length=100)),
                ('label', models.CharField(max_length=100, verbose_name='Libellé')),
                ('count_type', models.PositiveIntegerField(default=0, verbose_name="Nombre de ce type d'équipement")),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('services', models.ManyToManyField(related_name='equipment_types', through='company.Equipment', to='company.Service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_equiment_types', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Type d'équipements",
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='equipment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipments', to='company.EquipmentType', verbose_name="Type d'équipement associé"),
        ),
        migrations.AddField(
            model_name='equipment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipments', to='company.Service', verbose_name='Service associé'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_equipements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employeerestraint',
            name='restraint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_restraints', to='company.Restraint', verbose_name='Elément de retenue concerné'),
        ),
        migrations.AddField(
            model_name='employeerestraint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_employee_restraints', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employeeresponsability',
            name='responsability',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_responsabilities', to='company.Responsability', verbose_name='Responsabilité concerné'),
        ),
        migrations.AddField(
            model_name='employeeresponsability',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_employee_responsabilities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='company.Function', verbose_name='Fonction concernée'),
        ),
        migrations.AddField(
            model_name='employee',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='company.Grade', verbose_name='Grade concerné'),
        ),
        migrations.AddField(
            model_name='employee',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='company.Index', verbose_name='Indice concernée'),
        ),
        migrations.AddField(
            model_name='employee',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='company.Service', verbose_name='Service concerné'),
        ),
        migrations.AddField(
            model_name='employee',
            name='structure',
            field=models.ManyToManyField(related_name='employees', through='company.Contract', to='company.Structure'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contracts', to='company.Employee', verbose_name='Employé(e) si concerné(e)'),
        ),
        migrations.AddField(
            model_name='contract',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contracts', to='company.CompanyPartner', verbose_name='Partenaire si concerné(e)'),
        ),
        migrations.AddField(
            model_name='contract',
            name='structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contracts', to='company.Structure', verbose_name='Structure concernée'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CompanyPartnerType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_partner_types', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Types de partenaire',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='companypartner',
            name='partner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partners', to='company.CompanyPartnerType', verbose_name='Type de partenariat associé'),
        ),
        migrations.AddField(
            model_name='companypartner',
            name='structures',
            field=models.ManyToManyField(related_name='partners', through='company.Contract', to='company.Structure'),
        ),
        migrations.AddField(
            model_name='companypartner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_partners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basicsalary',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='basic_salaries', to='company.Grade', verbose_name='Grade concerné'),
        ),
        migrations.AddField(
            model_name='basicsalary',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='basic_salaries', to='company.Index', verbose_name='Indice concernée'),
        ),
        migrations.AddField(
            model_name='basicsalary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_basic_salaries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_date', models.DateField(auto_now_add=True, verbose_name='Date de la promotion')),
                ('slug', models.SlugField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='company.Employee', verbose_name='Employé(e) concerné(e)')),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='company.Function', verbose_name='Fonction concernée')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='company.Grade', verbose_name='Grade concerné')),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='company.Index', verbose_name='Indice concerné')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='company.Service', verbose_name='Service concerné')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_promotions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Salaires de base',
                'ordering': ['created_at'],
                'unique_together': {('employee', 'grade', 'index', 'service', 'function', 'created_at')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='employeerestraint',
            unique_together={('employee', 'restraint')},
        ),
        migrations.AlterUniqueTogether(
            name='employeeresponsability',
            unique_together={('employee', 'responsability')},
        ),
        migrations.AlterUniqueTogether(
            name='contract',
            unique_together={('structure', 'partner')},
        ),
        migrations.AlterUniqueTogether(
            name='basicsalary',
            unique_together={('grade', 'index')},
        ),
    ]