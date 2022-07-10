# Generated by Django 4.0.4 on 2022-07-09 21:50

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0044_task_email_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='decision',
            field=models.CharField(choices=[('---', '---'), ('Agreed', 'Agreed'), ('Decline', 'Decline')], default='---', help_text='\n        Select "Agreed" to indicate you are in Agreement with what has been proposed in this ServiceFlow.\n\n        Select "Declined" to indicate that you are not in Agreement.', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='decision_comments',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='emailcampaign',
            name='subject',
            field=models.CharField(blank=True, help_text='Enter a subject for the email campaign. \nNote that in the interest of readability that the subject is limited to 60 characters.', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='book_text_impacted',
            field=models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes')], default='---', help_text='Select "Yes" if you believe that the changes made will also need to be made in book files. \n\n        Select "No" if you believe that this observation only has an impact in the Library Record. For example, if a \n        hyperlink is broken this would have no impact upon book copy. \nIf you are uncertain if the book text will be \n        impacted select "Yes".', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, choices=[('---', '---'), ('Decision', 'Decision'), ('Library Observation', 'Library Observation'), ('Book Edit', 'Book Edit'), ('Email Campaign', 'Email Campaign')], default='---', max_length=50, null=True),
        ),
    ]