from django.db import models
from django.urls import reverse

from datetime import date

from tinymce.models import HTMLField


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


# ####################### Cosmic Author #######################
class CosmicAuthor(models.Model):
    """Cosmic Authors are associated with library records."""
    author = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'author',
        ]

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse('author', kwargs={'pk': self.pk})


# ####################### Tag #######################
class Tag(models.Model):
    """Tags are associated with library records."""
    tag = models.CharField(
        max_length=100,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        verbose_name_plural = 'Discourse Series'

    def __str__(self):
        return self.discourse_series

    def get_absolute_url(self):
        return reverse('discourse-series-detail', kwargs={'pk': self.pk})


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
        default=''
    )
    part_number = models.IntegerField(
        blank=True,
        null=True,
    )
    collection_order_number = models.IntegerField(
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
        verbose_name='Discourse series title'
    )
    principal_cosmic_author = models.ForeignKey(
        CosmicAuthor,
        related_name='principal_cosmic_author',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Principal author',
    )
    supporting_cosmic_authors = models.ManyToManyField(
        CosmicAuthor,
        blank=True,
        verbose_name='Supporting authors',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    language = models.CharField(
        max_length=20,
        choices=LIBRARY_RECORD_LANGUAGE,
        default='English'
    )
    date_communicated = models.DateField(default=date.today)
    year_communicated = models.IntegerField(
        null=True,
        blank=True,
    )
    pdf_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    doc_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    mp3_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'date_communicated',
        ]

    def __str__(self):
        # return self.title
        return f'Part {self.part_number} - {self.discourse_series} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'

    def get_absolute_url(self):
        return reverse('library-record', kwargs={'pk': self.pk})
