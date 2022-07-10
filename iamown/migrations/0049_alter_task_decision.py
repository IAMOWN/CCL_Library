# Generated by Django 4.0.4 on 2022-07-10 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0048_alter_task_book_text_impacted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='decision',
            field=models.CharField(blank=True, choices=[('Agreed', 'Agreed'), ('Revise', 'Revise'), ('Decline', 'Decline')], help_text='\n        Select "Agreed" to indicate you are in Agreement with what has been proposed in this ServiceFlow.\n\n        Select "Declined" to indicate that you are not in Agreement.', max_length=20, null=True),
        ),
    ]