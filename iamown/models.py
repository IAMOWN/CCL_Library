from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import (
    Profile,
)

from datetime import date

from tinymce.models import HTMLField

# ####################### CONSTANTS #######################
TASK_STATUS_CHOICES = [
    ('1) Not started', '1) Not started'),
    ('2) In progress', '2) In progress'),
    ('3) Deferred', '3) Deferred'),
    ('Completed', 'Completed'),
]
TASK_PRIORITY_CHOICES = [
    ('1) High', '1) High'),
    ('2) Normal', '2) Normal'),
    ('3) Low', '3) Low'),
]
TASK_TYPE_CHOICES = [
    ('---', '---'),
    ('Library Observation', 'Library Observation'),
]
SERVICE_GROUP_TYPES = [
    ('---', '---'),
    ('1) Esoteric', '1) Esoteric'),
    ('2) Exoteric', '2) Exoteric'),
]
SERVICE_GROUP_STATUS = [
    ('1) Active', '1) Active'),
    ('2) Inactive', '2) Inactive'),
]


# ####################### Service Group #######################
class ServiceGroup(models.Model):
    """Service Groups within the human collective of the EGA Divine Plan."""
    service_group = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        default=''
    )
    purpose = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    qualified_intentions = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    service_group_type = models.CharField(
        max_length=20,
        choices=SERVICE_GROUP_TYPES,
        default='---'
    )
    service_group_status = models.CharField(
        max_length=20,
        choices=SERVICE_GROUP_STATUS,
        default='1) Active'
    )
    dear_souls_in_service_group = models.ManyToManyField(
        Profile,
        verbose_name='Dear Souls in the service group',
        related_name='profiles_in_service_group',
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.service_group

    class Meta:
        verbose_name_plural = 'Service Groups'
        verbose_name = 'Service Group'
        ordering = [
            'service_group_type',
            'service_group',
        ]

    def get_absolute_url(self):
        return reverse('service-group', kwargs={'pk': self.pk})


# ####################### Tasks #######################
class Task(models.Model):
    """Allows for independent tasks for any given user or service group"""
    task_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    task_description = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='1) Not started')
    task_priority = models.CharField(
        max_length=20,
        choices=TASK_PRIORITY_CHOICES,
        default='2) Normal',
        help_text="Selecting '1) High' will not only place the task higher in the task list."
    )
    due_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        help_text='Enter the date you are aiming to complete this task by.'
    )
    task_type = models.CharField(
        choices=TASK_TYPE_CHOICES,
        null=True,
        blank=True,
        max_length=50,
        default='---',
    )
    related_task = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='approval_task',
        on_delete=models.CASCADE
    )
    assigned_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='profile_in_library_task',
        verbose_name='Assigned Dear Soul',
    )
    assigned_service_group = models.ForeignKey(
        ServiceGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='service_group_assigned_task',
    )
    task_history_log = HTMLField(
        default='',
        blank=True,
        null=True,
    )

    task_created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.task_title} ** Status - {self.task_status} ({self.id})'

    class Meta:
        ordering = [
            'task_status',
            'task_priority',
            'due_date',
        ]

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})
        # return reverse('tasks')
