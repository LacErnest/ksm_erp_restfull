<<<<<<< HEAD:partner/migrations/0001_initial.py
# Generated by Django 3.0.7 on 2020-08-21 09:32
=======
# Generated by Django 3.0.7 on 2020-08-01 02:40
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea:partner/migrations/0001_migration_partner.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import partner.models
<<<<<<< HEAD:partner/migrations/0001_initial.py
=======
import phone_field.models
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea:partner/migrations/0001_migration_partner.py
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EligiblePrice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Prix éligibles',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExemptTaxe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
            ],
            options={
                'verbose_name_plural': 'Taxes exemptées',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=100)),
                ('matricule', models.CharField(max_length=50, unique=True, verbose_name='Matricule')),
                ('state', models.CharField(max_length=50, null=True, verbose_name='Statut')),
                ('photo', models.ImageField(upload_to='photos/', verbose_name='Photo / Logo')),
                ('social_reason', models.CharField(max_length=100, null=True, verbose_name='Raison sociale')),
                ('juridical_form', models.CharField(max_length=100, null=True, verbose_name='Forme juridique')),
                ('society', models.CharField(max_length=100, null=True, verbose_name='Entreprise')),
                ('description', models.TextField(max_length=200, verbose_name='Description du partenariat')),
                ('family', models.CharField(max_length=100, null=True, verbose_name='Famille')),
                ('city', models.CharField(max_length=50, verbose_name='Ville')),
                ('country', models.CharField(max_length=50, verbose_name='Pays')),
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
            name='PartnerAdresse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Longitude')),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Latitude')),
                ('default_delivery_address', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=3, validators=[partner.models.PartnerAdresse.validate_is_default], verbose_name='Definir comme adresse par défaut')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partner_adresse', to='partner.Partner', verbose_name='Partenaire associé(e)')),
            ],
            options={
                'verbose_name_plural': 'Adresses de partenaires',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PartnerPaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('value', models.CharField(max_length=100, verbose_name='N° Téléphone/ N° Compte')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.Partner', verbose_name='Partenaire associé')),
            ],
            options={
                'verbose_name_plural': 'Moyens de payement des partenaires',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TypeAdresse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partners', models.ManyToManyField(related_name='type_adresses', through='partner.PartnerAdresse', to='partner.Partner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_type_adresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Types d'adresse",
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partners', models.ManyToManyField(related_name='prices', through='partner.EligiblePrice', to='partner.Partner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_prices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Prix',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('image', models.ImageField(upload_to='images/', verbose_name='Image')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partners', models.ManyToManyField(related_name='payment_methods', through='partner.PartnerPaymentMethod', to='partner.Partner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Moyens de payement',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PartnerType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_partner_types', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Types de partenaire',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PartnerTax',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='Libellé')),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partners', models.ManyToManyField(related_name='taxes', through='partner.ExemptTaxe', to='partner.Partner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_taxes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Taxes',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='partnerpaymentmethod',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.PaymentMethod', verbose_name='Moyen de payement associé'),
        ),
        migrations.AddField(
            model_name='partnerpaymentmethod',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_partner_payment_methods', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partneradresse',
            name='type_adresse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partner_adresse', to='partner.TypeAdresse', verbose_name="Type d'adresse associé(e)"),
        ),
        migrations.AddField(
            model_name='partneradresse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_partner_adresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partner',
            name='partner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partners', to='partner.PartnerType', verbose_name='Type de partenariat associé'),
        ),
        migrations.AddField(
            model_name='partner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exempttaxe',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.Partner', verbose_name='Partenaire associé'),
        ),
        migrations.AddField(
            model_name='exempttaxe',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.PartnerTax', verbose_name='Taxe associée'),
        ),
        migrations.AddField(
            model_name='exempttaxe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_exempt_taxes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eligibleprice',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.Partner', verbose_name='Partenaire associé'),
        ),
        migrations.AddField(
            model_name='eligibleprice',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.Price', verbose_name='Prix associé'),
        ),
        migrations.AddField(
            model_name='eligibleprice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_eligible_prices', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=100)),
                ('telephone', phone_field.models.PhoneField(max_length=31, verbose_name='N° Téléphone')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('fax', models.CharField(max_length=50, null=True, verbose_name='Fax')),
                ('postal_code', models.CharField(max_length=50, null=True, unique=True, verbose_name='Code postal')),
                ('web_site', models.URLField(help_text='https://www.yoyobb.com', max_length=50, null=True, verbose_name='Site web')),
                ('whatsapp_id', phone_field.models.PhoneField(help_text='Obligatoire', max_length=31, verbose_name='N° Téléphone watsapp')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Date de dernière modification')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='partner.Partner', verbose_name='Partenaire associé')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patner_contacts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Contacts',
                'ordering': ['created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='partnerpaymentmethod',
            unique_together={('partner', 'payment_method')},
        ),
        migrations.AlterUniqueTogether(
            name='exempttaxe',
            unique_together={('partner', 'tax')},
        ),
        migrations.AlterUniqueTogether(
            name='eligibleprice',
            unique_together={('partner', 'price')},
        ),
    ]