# Generated by Django 4.0.4 on 2022-07-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0045_alter_cosmicauthor_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collection',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
