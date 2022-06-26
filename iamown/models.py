from django.db import models
from django.contrib.auth.models import User

from datetime import date

from tinymce.models import HTMLField

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


# ####################### Tasks #######################
class Task(models.Model):
    """Task model. Captures the independent tasks for any given user or service group
    Related to User/Profile as each task belongs to a user."""
    task_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    assigned_dear_soul = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # models.SET_NULL to not delete
        blank=True,
        verbose_name='Assigned to'
    )
    task_description = HTMLField(
        default='',
        blank=True,
        null=True,
    )
    # assigned_team = models.CharField(
    #     max_length=50,
    #     null=True,
    #     blank=True,
    #     default='',
    #     help_text='''
    #     If you have many teams collaborating in Whurthy you can enter in the Team name. This will allow you to
    #     filter by team in the task list.
    #     '''
    # )
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='1) Not started')
    task_priority = models.CharField(
        max_length=20,
        choices=TASK_PRIORITY_CHOICES,
        default='2) Normal',
        help_text="Selecting '1) High' will not only place the task higher in the task list but will also "
                  "result in it showing in the 'My High Priority' section of the dashboard."
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