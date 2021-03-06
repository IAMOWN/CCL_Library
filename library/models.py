from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date

from tinymce.models import HTMLField

from users.models import (
    Profile,
)


# ####################### Date logic #######################
def current_year():
    return date.today().year


# ####################### CHOICE CONSTANTS #######################
LIBRARY_RECORD_TYPE = [
    ('Discourse', 'Discourse'),
    ('Book', 'Book'),
    ('Cosmic Review', 'Cosmic Review'),
    ('Invocation', 'Invocation'),
    ('Petition', 'Petition'),
]

LIBRARY_RECORD_LANGUAGE = [
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('French', 'French'),
    ('Chinese', 'Chinese'),
    ('Dutch', 'Dutch'),
    ('German', 'German'),
    ('Japanese', 'Japanese'),
    ('Norwegian', 'Norwegian'),
    ('Polish', 'Polish'),
    ('Portuguese', 'Portuguese'),
    ('Sanskrit', 'Sanskrit'),
    ('Swedish', 'Swedish'),
]

READING_PROGRESS = [
    ('---', '---'),
    ('1) On Reading List', '1) On Reading List'),
    ('2) Reading In Progress', '2) Reading In Progress'),
    ('3) Completed Reading', '3) Completed Reading'),
]

OBSERVATION_TYPE = [
    ('Typo', 'Typo'),
    ('Image', 'Image'),
    ('Broken Link', 'Broken Link'),
    ('Other', 'Other'),
]


# ####################### Master #######################
class CosmicAuthor(models.Model):
    """Cosmic Authors are associated with library records."""
    author = models.CharField(
        max_length=100,
        default='',
        unique=True,
        verbose_name='master'
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'author',
        ]
        verbose_name_plural = 'Masters'

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse('master', kwargs={'pk': self.pk})


# ####################### Tag #######################
class Tag(models.Model):
    """Tags are associated with library records."""
    tag = models.CharField(
        max_length=100,
        unique=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'tag',
        ]

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'pk': self.pk})


# ####################### Discourse Series #######################
class DiscourseSeries(models.Model):
    """Discourse Series provides a list of series to support views and search"""
    discourse_series = models.CharField(
        max_length=100,
        unique=True,
        default='',
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'discourse_series',
        ]
        verbose_name_plural = 'Series'

    def __str__(self):
        return self.discourse_series

    def get_absolute_url(self):
        return reverse('discourse-series-detail', kwargs={'pk': self.pk})


# ####################### Collection #######################
class Collection(models.Model):
    """Discourses can be a part of one or many Collections. The Collection model is referred to through the
    CollectionOrder Many to Many relationship."""
    collection = models.CharField(
        max_length=100,
        unique=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'collection',
        ]

    def __str__(self):
        return self.collection

    def get_absolute_url(self):
        return reverse('collection', kwargs={'pk': self.pk})


# ####################### Library Record #######################
class LibraryRecord(models.Model):
    """Library records capture all Discourses for the CCL Web Application."""
    library_record_type = models.CharField(
        max_length=20,
        choices=LIBRARY_RECORD_TYPE,
        default='Discourse'
    )
    title = models.CharField(
        max_length=200,
        default='',
    )
    part_number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    invocation = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    text = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    benediction = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    discourse_series = models.ForeignKey(
        DiscourseSeries,
        related_name='discourse_series_title',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Discourse series title',
        help_text='Select the Series with which this record was originally communicated, or associated with.'
    )
    principal_cosmic_author = models.ForeignKey(
        CosmicAuthor,
        related_name='principal_cosmic_author',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Master',
        help_text='Select the principal, or primary, Master of this record.'
    )
    supporting_cosmic_authors = models.ManyToManyField(
        CosmicAuthor,
        blank=True,
        verbose_name='Supporting Masters',
        help_text='If applicable, select one or more, supporting Masters that contributed to the record.'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    language = models.CharField(
        max_length=20,
        choices=LIBRARY_RECORD_LANGUAGE,
        default='English',
        help_text='By default all records are assumed to be in English. If a translated version of a record is uploaded '
                  'then select the applicable language.'
    )
    date_communicated = models.DateField(
        default=date.today,
        help_text='Enter the date that the record was originally communicated.'
    )
    pdf_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='',
        help_text='''Enter the URL for the PDF file in the soul-synthesis-storage S3 server. This url is used to 
        present the downloadable PDF link in the library record.'''
    )
    doc_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='',
    )
    mp3_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='',
        help_text='''Enter the URL for the MP3 file in the soul-synthesis-storage S3 server. This url is used to 
        present the downloadable audio file in the library record.''',
    )
    book_urls = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='''Enter any URLs related directly to book editing (such as links to the docx/pdf files stored in 
        ProtonDrive. This information is used to support book editing activities and is not used within the CCL Library.
        '''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'date_communicated',
        ]
        verbose_name_plural = 'Library Records'

        unique_together = ('discourse_series', 'part_number',)

    def __str__(self):
        # return f'Part {self.part_number} - {self.discourse_series} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'
        if self.part_number and self.discourse_series:
            return f'Part {self.part_number} - {self.discourse_series} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'
        elif self.discourse_series:
            return f'{self.discourse_series} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'
        else:
            return f'{self.title} - {self.principal_cosmic_author} - {self.date_communicated}'

    def get_absolute_url(self):
        return reverse('library-record', kwargs={'pk': self.pk})


# ####################### Record Read #######################
class RecordRead(models.Model):
    record_read = models.ForeignKey(
        LibraryRecord,
        related_name='record_read_by_user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reader = models.ForeignKey(
        User,
        related_name='reader_of_record',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    client_ip = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default='',
    )
    date_read = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            '-date_read',
        ]
        verbose_name_plural = 'Records Read'

    def __str__(self):
        if self.reader:
            return f'"{self.record_read.title}" read by {self.reader} on {self.date_read.strftime("%Y-%m-%d %H:%M")}'
        else:
            return f'"{self.record_read.title}" read from the IP address "{self.client_ip}" on {self.date_read.strftime("%Y-%m-%d %H:%M")}'


# ####################### Collection Order #######################
class CollectionOrder(models.Model):
    """Discourses can be a part of one or many Collections. The Collection Order allows the tracking of the collection
    order for every Discourse within a Collection."""
    collection = models.ForeignKey(
        Collection,
        related_name='collection_in_collection_order',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Collection'
    )
    record = models.ForeignKey(
        LibraryRecord,
        related_name='record_in_collection_order',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Library record',
    )
    order_number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    # class Meta:
    #     ordering = [
    #         'collection',
    #     ]

    def __str__(self):
        return f'Part {self.record.part_number} - {self.record.discourse_series} - {self.record.title} - {self.record.principal_cosmic_author} - {self.record.date_communicated}'


# ####################### Reading Progress #######################
class ReadingProgress(models.Model):
    record = models.ForeignKey(
        LibraryRecord,
        related_name='record_in_reading_progress',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Library record',
    )
    dear_soul = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_in_reading_progress',
    )
    reading_progress = models.CharField(
        max_length=30,
        choices=READING_PROGRESS,
        default='---'
    )
    date_added = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    date_started = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    date_completed = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    date_latest = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    reading_progress_log = HTMLField(
        null=True,
        blank=True,
    )
    total_readings = models.PositiveIntegerField(
        default= 0,
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'reading_progress',
        ]
        verbose_name_plural = 'Reading Progress'

        unique_together = ('record', 'dear_soul',)

    def __str__(self):
        return (
            f"{self.record.title} - {self.reading_progress} ({self.dear_soul} -"
            f" {self.record_id})"
        )

    # def get_absolute_url(self):
    #     return reverse('library-record', kwargs={'pk': self.pk})


# ####################### Record Observation #######################
class LibraryObservation(models.Model):
    observation_type = models.CharField(
        max_length=30,
        choices=OBSERVATION_TYPE,
        default='Typo',
        null=True,
        blank=True,
        help_text='''Please select the applicable observation type.'''
    )
    library_record = models.ForeignKey(
        LibraryRecord,
        related_name='record_in_observation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    observer = models.ForeignKey(
        Profile,
        related_name= 'profile_for_library_observation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    typo = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='',
        help_text='''Please copy/paste in the incorrect text as observed from the record.'''
    )
    suggested_correction = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='',
        help_text='''Please enter in your suggested correction.''',
    )
    image_observation = HTMLField(
        null=True,
        blank=True,
        help_text='''Please describe your observation about images in the record, such as if an image is missing, not 
        displaying correctly and showing as broken.'''
    )
    link_observation = HTMLField(
        null=True,
        blank=True,
        help_text='''Please describe what happens when you click the link. Is the link broken? Does it take you to a 
        webpage you were not expecting?'''
    )
    header_title_observation = HTMLField(
        null=True,
        blank=True,
        help_text='''Please describe what is not correct in the Header or Title of the record.'''
    )
    general_observation = HTMLField(
        null=True,
        blank=True,
        help_text='''Please describe what you are observing and what you believe could be changed or corrected.'''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.observation_type} - {self.observer} - {self.date_created}'

    def get_absolute_url(self):
        # return reverse('library-record', kwargs={'pk': self.pk})
        return reverse('library-record', kwargs={'pk': self.library_record_id})
