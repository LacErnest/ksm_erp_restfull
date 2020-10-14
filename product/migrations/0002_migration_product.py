# Generated by Django 3.0.7 on 2020-09-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_migration_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productillustration',
            name='image',
        ),
        migrations.RemoveField(
            model_name='productillustration',
            name='video',
        ),
        migrations.AddField(
            model_name='productillustration',
            name='illustration',
            field=models.FileField(default='images/téléchargement_4.jpg', upload_to='illustrations/', verbose_name='Image/Vidéo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productillustration',
            name='type_illustration',
            field=models.CharField(choices=[('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO')], default='IMAGE', max_length=10, verbose_name="Type de l'illustration"),
        ),
    ]