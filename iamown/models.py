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
    ('Decision', 'Decision'),
    ('Library Observation', 'Library Observation'),
    ('Book Edit', 'Book Edit'),
    ('Email Campaign', 'Email Campaign'),
    ('Email Campaign 2', 'Email Campaign 2'),
    ('Email Campaign 2 - Revise', 'Email Campaign 2 - Revise'),
]
TASK_DECISION_CHOICES = [
    ('Agreed', 'Agreed'),
    ('Revise', 'Revise'),
    ('Decline', 'Decline'),
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
    ('No', 'No'),
    ('Yes', 'Yes'),
]
APPLICATION_CHOICES = [
    ('Library', 'Library'),
    ('IAMOWN', 'IAMOWN'),
    ('Users', 'Users'),
    ('Other', 'Other'),
]
SCOPE_CHOICES = [
    ('Internal', 'Internal'),
    ('External', 'External'),
    ('Both', 'Both'),
]
EMAIL_CAMPAIGN_STATUS_CHOICES = [
    ('1) Created', '1) Created'),
    ('2) In progress', '2) In progress'),
    ('3) Declined', '3) Declined'),
    ('Sent', 'Sent'),
]


# ####################### Service Group #######################
class ServiceGroup(models.Model):
    """Service Groups within the human collective of the EGA Divine Plan."""
    service_group = models.CharField(
        max_length=150,
        unique=True,
        default=''
    )
    purpose = HTMLField(
        default='',
    )
    qualified_intentions = HTMLField(
        default='',
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

    class Meta:
        verbose_name_plural = 'Service Groups'
        verbose_name = 'Service Group'
        ordering = [
            'service_group_type',
            'service_group',
        ]

    def __str__(self):
        return self.service_group

    def get_absolute_url(self):
        return reverse('service-group', kwargs={'pk': self.pk})


# ####################### Audiences #######################
class Audience(models.Model):
    """
    Audience model. Captures the list of mailing list audiences. Newsletter is sent to an audience.
    """
    audience = models.CharField(
        unique=True,
        max_length=100,
        help_text='Enter the audience name.'
    )
    scope = models.CharField(
        choices=SCOPE_CHOICES,
        max_length=20,
        default='Internal',
    )
    audience_notes = HTMLField(
        default='',
        help_text='If applicable, enter any notes about this audience.'
    )
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.audience

    def get_absolute_url(self):
        return reverse('audience-entry', kwargs={'pk': self.pk})


# ####################### Mailing List #######################
class MailingList(models.Model):
    audience = models.ForeignKey(
        Audience,
        on_delete=models.CASCADE,
        related_name='audience_in_mailing_list',
        default='',
    )
    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default='',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_in_mailing_list',
    )
    subscribed = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='Yes',
    )
    mailing_list_log = HTMLField(
        default='',
    )

    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = [
            '-subscribed',
            'audience',
            'user',
            'email',
        ]
        verbose_name_plural = 'Mailing List'
        verbose_name = 'Mailing List'

    def __str__(self):
        if self.email:
            return f'{self.audience}: {self.email}'
        else:
            return f'{self.audience}: {self.user.username}'

    def get_absolute_url(self):
        return reverse('mailing-list-entry', kwargs={'pk': self.pk})


# ####################### Email Campaign #######################
class EmailCampaign(models.Model):
    audience = models.ForeignKey(
        Audience,
        on_delete=models.CASCADE,
        related_name='audience_in_email_campaign',
        default='',
        help_text='Select the targeted audience for this email campaign.'
    )
    subject = models.CharField(
        max_length=60,
        help_text='Enter a subject for the email campaign. \nNote that in the interest of readability that the '
                  'subject is limited to 60 characters.',
        default='',
    )
    message = HTMLField(
        default='',
        help_text='Enter the email message you intend on sending.',
    )
    ready_to_send = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
        help_text='By default, this is set to "No". When you are ready to begin the Email Campaign ServiceFlow then '
                  'change this to "Yes".'
    )
    test_email_sent = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
    )
    sender_accepted_test = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
    )
    sender = models.ForeignKey(
        User,
        related_name= 'user_in_email_campaign',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    sender_email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    review_email_sent = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
    )
    number_of_reviewers = models.PositiveSmallIntegerField(
        default=0,
    )
    number_of_accepted_reviews = models.PositiveSmallIntegerField(
        default=0,
    )
    number_of_declined_reviews = models.PositiveSmallIntegerField(
        default=0,
    )
    email_campaign_sent = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
    )
    send_status = models.CharField(
        choices=EMAIL_CAMPAIGN_STATUS_CHOICES,
        null=True,
        blank=True,
        max_length=20,
        default='1) Created',
    )

    email_send_log = HTMLField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = [
            'send_status',
        ]
        unique_together = ['audience', 'subject']
        verbose_name_plural = 'Email Campaign'
        verbose_name = 'Email Campaigns'

    def __str__(self):
        return f"{self.audience} - {self.subject} ({self.date_created.strftime('%Y-%m-%d')})"


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
        help_text='Task Priority is used to help determine the order of displayed tasks. The ordering of tasks is by: '
                  'Status, then Priority, and finally Due Date. Selecting "1) High" presents tasks higher in the list, '
                  'while selecting "3) Low" is a way of moving longer-term tasks to the end of the task list.'
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
        default='No',
        help_text='''Select "Yes" if you believe that the changes made will also need to be made in book files. \n
        Select "No" if you believe that this observation only has an impact in the Library Record. For example, if a 
        hyperlink is broken this would have no impact upon book copy. \nIf you are uncertain if the book text will be 
        impacted select "Yes".'''
    )
    email_campaign = models.ForeignKey(
        EmailCampaign,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='email_campaign_in_task',
    )
    email_campaign_test_accepted = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default='No',
    )

    decision = models.CharField(
        choices=TASK_DECISION_CHOICES,
        max_length=20,
        null=True,
        blank=True,
        help_text='''
        Select "Agreed" to indicate you are in Agreement with what has been proposed in this ServiceFlow.\n
        Select "Declined" to indicate that you are not in Agreement.'''
    )
    decision_comments = HTMLField(
        null=True,
        blank=True,
        default='',
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

    class Meta:
        ordering = [
            'task_status',
            'task_priority',
            'due_date',
        ]

    def __str__(self):
        return f'{self.task_title} (Status: {self.task_status}) {self.id}'

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
        null=True,
        blank=True,
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
        default='',
        null=True,
        blank=True,
        help_text="If applicable. enter the process code for this process activity. The recommended format should be "
                  "abbreviations of the organism's name and the process name. There is a 12 character limit for the "
                  "Process Code."
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
        default='library/views.py',
        max_length=100,
        null=True,
        blank=True,
        help_text='If applicable, enter the specific file path and file name within the Django web app.'
    )

    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = [
            'task_name'
        ]
        verbose_name_plural = 'LEE'
        verbose_name = 'LEE'

    def __str__(self):
        return f'{self.task_name} ({self.application})'

    def get_absolute_url(self):
        return reverse('lee-entry', kwargs={'pk': self.pk})


# ####################### PEeP #######################
class PEeP(models.Model):
    """
    PEeP (Process Expertise Profile) model. Captures Team members by function/responsibility for task
    assignment. Related to User as each entry relates to a Team member.
    """
    functional_activity = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True,
        help_text='Enter the functional activity. Note: the application will only be able to act on this record if the '
                  'applicable feature has been built into the application. However, please feel free to enter PEeP '
                  'records for your reference, and to identify future ServiceFlow automation opportunities.'
    )
    detailed_description = HTMLField(
        null=True,
        blank=True,
        help_text='If applicable, enter a description for this record. While this description will not be utilized '
                  'directly as a part of a ServiceFlow, providing a description in this field should support '
                  'understanding when and why this particular record is used, and what ServiceFlow it supports.'
    )
    dear_soul_responsible = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dear_soul_in_peep',
        help_text='Select the Dear Soul responsible for this task. Please note that this required field is integral to '
                  'ServiceFlow automation in that information in both this field and Process function is used to, where '
                  'appropriate, assign tasks as a part of ServiceFlow.'
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='service_group_in_PEeP',
        help_text='If this PEeP entry belongs to a ServiceFlow associated with a Service Group then select them. This '
                  'field is optional and is use for reference only.'
    )
    process_code = models.CharField(
        max_length=20,
        default='',
        null=True,
        blank=True,
        help_text="Enter the process code for this process activity. The recommended format should be abbreviations of "
                  "the organization's name and the process name. For example, the Whurthy employee on-boarding "
                  "process could have the process code of LFON. There is a limit of 20 characters for the Process Code."
    )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = [
            'functional_activity',
        ]
        verbose_name_plural = 'PEeP'
        verbose_name = 'PEeP'
        unique_together = ['functional_activity', 'dear_soul_responsible']

    def __str__(self):
        return self.process_function

    def get_absolute_url(self):
        return reverse('peep-entry', kwargs={'pk': self.pk})
