# Generated by Django 4.0.4 on 2022-07-14 18:35

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0061_alter_emailcampaign_send_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='mailing_list_log',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AlterField(
            model_name='audience',
            name='audience_notes',
            field=tinymce.models.HTMLField(default='', help_text='If applicable, enter any notes about this audience.'),
        ),
        migrations.AlterField(
            model_name='emailcampaign',
            name='message',
            field=tinymce.models.HTMLField(default='', help_text='Enter the email message you intend on sending.'),
        ),
        migrations.AlterField(
            model_name='emailcampaign',
            name='subject',
            field=models.CharField(default='', help_text='Enter a subject for the email campaign. \nNote that in the interest of readability that the subject is limited to 60 characters.', max_length=60),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='subscribed',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='Yes', max_length=10),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='purpose',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='qualified_intentions',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='service_group',
            field=models.CharField(default='', max_length=150, unique=True),
        ),
    ]