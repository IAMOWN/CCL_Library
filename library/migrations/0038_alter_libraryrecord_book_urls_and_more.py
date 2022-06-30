# Generated by Django 4.0.4 on 2022-06-30 21:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0037_libraryrecord_book_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryrecord',
            name='book_urls',
            field=tinymce.models.HTMLField(blank=True, default='', help_text='Enter any URLs related directly to book editing (such as links to the docx/pdf files stored in \n        ProtonDrive. This information is used to support book editing activities and is not used within the CCL Library.\n        ', null=True),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='date_communicated',
            field=models.DateField(default=datetime.date.today, help_text='Enter the date that the record was originally communicated.'),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='discourse_series',
            field=models.ForeignKey(blank=True, help_text='Select the Series with which this record was originally communicated, or associated with.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discourse_series_title', to='library.discourseseries', verbose_name='Discourse series title'),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Spanish', 'Spanish'), ('French', 'French'), ('Chinese', 'Chinese'), ('Dutch', 'Dutch'), ('German', 'German'), ('Japanese', 'Japanese'), ('Norwegian', 'Norwegian'), ('Polish', 'Polish'), ('Portuguese', 'Portuguese'), ('Sanskrit', 'Sanskrit'), ('Swedish', 'Swedish')], default='English', help_text='By default all records are assumed to be in English. If a translated version of a record is uploaded then select the applicable language.', max_length=20),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='mp3_url',
            field=models.CharField(blank=True, default='', help_text='Enter the URL for the MP3 file in the soul-synthesis-storage S3 server. This url is used to \n        present the downloadable audio file in the library record.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='pdf_url',
            field=models.CharField(blank=True, default='', help_text='Enter the URL for the PDF file in the soul-synthesis-storage S3 server. This url is used to \n        present the downloadable PDF link in the library record.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='principal_cosmic_author',
            field=models.ForeignKey(blank=True, help_text='Select the principal, or primary, Master of this record.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='principal_cosmic_author', to='library.cosmicauthor', verbose_name='Master'),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='supporting_cosmic_authors',
            field=models.ManyToManyField(blank=True, help_text='If applicable, select one or more, supporting Masters that contributed to the record.', to='library.cosmicauthor', verbose_name='Supporting Masters'),
        ),
    ]
