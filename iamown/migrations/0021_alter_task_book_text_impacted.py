# Generated by Django 4.0.4 on 2022-06-30 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0020_task_book_text_impacted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='book_text_impacted',
            field=models.CharField(blank=True, choices=[('---', '---'), ('No', 'No'), ('Yes', 'Yes')], default='---', max_length=10, null=True),
        ),
    ]
