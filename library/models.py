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


# ####################### Master #######################
class CosmicAuthor(models.Model):
    """Cosmic Authors are associated with library records."""
    author = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default='',
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

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse('master', kwargs={'pk': self.pk})


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


# ####################### Collection #######################
class Collection(models.Model):
    """Discourses can be a part of one or many Collections. The Collection model is referred to through the
    CollectionOrder Many to Many relationship."""
    collection = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default=''
    )

    class Meta:
        ordering = [
            'collection',
        ]

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse('collection', kwargs={'pk': self.pk})

    def __str__(self):
        return self.collection


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
        verbose_name='Discourse series title'
    )
    principal_cosmic_author = models.ForeignKey(
        CosmicAuthor,
        related_name='principal_cosmic_author',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Master',
    )
    supporting_cosmic_authors = models.ManyToManyField(
        CosmicAuthor,
        blank=True,
        verbose_name='Supporting Masters',
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
        if self.part_number and self.discourse_series:
            return f'Part {self.part_number} - {self.discourse_series} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'
        elif self.part_number:
            return f'Part {self.part_number} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'
        else:
            return f'{self.title} - {self.principal_cosmic_author} - {self.date_communicated}'


    def get_absolute_url(self):
        return reverse('library-record', kwargs={'pk': self.pk})


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
        verbose_name='Library record'
    )
    order_number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = [
            'collection',
        ]

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.collection}: {self.record} - {self.order_number}'
