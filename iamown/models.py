from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from users.models import (
    Profile,
)

from library.models import (
    LibraryRecord,
    LibraryObservation,
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
    ('Book Edit', 'Book Edit'),
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
YES_NO_CHOICES = [
    ('---', '---'),
    ('No', 'No'),
    ('Yes', 'Yes'),
]
APPLICATION_CHOICES = [
    ('Library', 'Library'),
    ('IAMOWN', 'IAMOWN'),
    ('Users', 'Users'),
    ('Other', 'Other'),
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
    actions_taken = HTMLField(
        default='',
        blank=True,
        null=True,
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
    library_observation = models.ForeignKey(
        LibraryObservation,
        null=True,
        blank=True,
        related_name='library_observation_in_library_task',
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
    library_record = models.ForeignKey(
        LibraryRecord,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='library_record_in_task',
    )
    library_task_description = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    library_task_actions_taken = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    book_urls_for_record = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    book_text_impacted = models.CharField(
        choices=YES_NO_CHOICES,
        null=True,
        blank=True,
        max_length=10,
        default='---',
        help_text='''Select "Yes" if you believe that the changes made will also need to be made in book files. Select 
        "No" if you believe that this observation only has an impact in the Library Record. For example, if a hyperlink 
        is broken this would have no impact upon book copy. If you are uncertain if the book text will be impacted select "Yes".'''
    )
    task_history_log = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    date_completed = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    task_created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.task_title} (Status: {self.task_status})'

    class Meta:
        ordering = [
            'task_status',
            'task_priority',
            'due_date',
        ]

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})
        # return reverse('tasks')


# ####################### LEE #######################
class LEE(models.Model):
    """
    Learned Experience Engine model. Captures process descriptions for tasks and form errors.
    """
    task_name = models.CharField(
        max_length=100,
        default='',
        unique=True,
        help_text='Enter the specific task name. This should not be changed once it has been coded into the application '
                  'as this will be used in task assignment. Do not change this value unless you know what you are doing.'
    )
    process_description = HTMLField(
        default='',
        help_text='Enter the process description for the task. Whatever is entered into this field will be the '
                  'process description provided for the task assignment/notification to the assignee.'
    )
    responsible_for_entry = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lEE_responsible_for_entry',
        help_text='If applicable, enter the Dear Soul responsible for this entry.'
    )
    process_code = models.CharField(
        max_length=12,
        default='LIB',
        null=True,
        blank=True,
        help_text="Enter the process code for this process activity. The recommended format should be abbreviations of "
                  "the organization's name and the process name. For example, the Whurthy employee on-boarding "
                  "process could have the process code of WON. There is a limit of 12 characters for the Process Code."
    )
    process_outcome = HTMLField(
        null=True,
        blank=True,
        help_text='If applicable, enter a description of the outcome of this activity.'
    )
    application = models.CharField(
        max_length=100,
        default='Library',
        choices=APPLICATION_CHOICES,
        help_text='Please select the application that this entry applies to.'
    )
    relevant_django_file = models.CharField(
        default='events/ views.py',
        max_length=100,
        null=True,
        blank=True,
        help_text='If applicable, enter the specific file path and file name within the Django web app.'
    )

    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.process_role} ({self.whurthy_application})'

    class Meta:
        ordering = [
            'task_name'
        ]
        verbose_name_plural = 'LEE'
        verbose_name = 'LEE'
