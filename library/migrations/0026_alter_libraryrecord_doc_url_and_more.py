# Generated by Django 4.0.4 on 2022-06-23 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0025_alter_collectionorder_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryrecord',
            name='doc_url',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='mp3_url',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='pdf_url',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
