from django.urls import path

from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    TaskCompletedList,
    TaskLibraryList,
    TaskLibraryDetail,
    TaskLibraryCompletedList,
    TaskLibraryCreate,
    TaskLibraryUpdate,
    TaskLibraryDelete,
    ServiceGroupList,
    ServiceGroupDetail,
    ServiceGroupCreate,
    ServiceGroupUpdate,
    ServiceGroupDelete,
    LEEListView,
    LEEDetailView,
    LEECreateView,
    LEEUpdateView,
    LEEDeleteView,
    PEePListView,
    PEePDetailView,
    PEePCreateView,
    PEePUpdateView,
    PEePDeleteView,
    AudienceListView,
    AudienceDetailView,
    AudienceCreateView,
    AudienceUpdateView,
    AudienceDeleteView,
    MailingListListView,
    MailingListDetailView,
    MailingListCreateView,
    MailingListUpdateView,
    MailingListDeleteView,
    EmailCampaignListView,
    EmailCampaignDetailView,
    EmailCampaignCreateView,
    EmailCampaignUpdateView,
    EmailCampaignDeleteView,
    unsubscribe,
)

urlpatterns = [
    # Tasks
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task_create/', TaskCreate.as_view(), name='task-create'),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('tasks/completed/', TaskCompletedList.as_view(), name='tasks-completed'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    # Library Tasks
    path('tasks/library/', TaskLibraryList.as_view(), name='tasks-library'),
    path('task/library/<int:pk>/', TaskLibraryDetail.as_view(), name='task-library'),
    path('task_create/library/', TaskLibraryCreate.as_view(), name='task-create-library'),
    path('task_update/library/<int:pk>/', TaskLibraryUpdate.as_view(), name='task-update-library'),
    path('tasks/completed/library/', TaskLibraryCompletedList.as_view(), name='tasks-completed-library'),
    path('task_delete/library/<int:pk>/', TaskLibraryDelete.as_view(), name='task-delete-library'),

    # Service Groups
    path('service_groups/', ServiceGroupList.as_view(), name='service-groups'),
    path('service_group/<int:pk>/', ServiceGroupDetail.as_view(), name='service-group'),
    path('service_group_create/', ServiceGroupCreate.as_view(), name='service-group-create'),
    path('service_group_update/<int:pk>/', ServiceGroupUpdate.as_view(), name='service-group-update'),
    path('service_group_delete/<int:pk>/', ServiceGroupDelete.as_view(), name='service-group-delete'),

    # LEE
    path('lee/', LEEListView.as_view(), name='lee'),
    path('lee/<int:pk>/', LEEDetailView.as_view(), name='lee-entry'),
    path('lee_create/', LEECreateView.as_view(), name='lee-create'),
    path('lee_update/<int:pk>/', LEEUpdateView.as_view(), name='lee-update'),
    path('lee_delete/<int:pk>/', LEEDeleteView.as_view(), name='lee-delete'),

    # PEeP
    path('peeps/', PEePListView.as_view(), name='peeps'),
    path('peep/<int:pk>/', PEePDetailView.as_view(), name='peep-entry'),
    path('peep_create/', PEePCreateView.as_view(), name='peep-create'),
    path('peep_update/<int:pk>/', PEePUpdateView.as_view(), name='peep-update'),
    path('peep_delete/<int:pk>/', PEePDeleteView.as_view(), name='peep-delete'),

    # Audiences
    path('audiences/', AudienceListView.as_view(), name='audiences'),
    path('audience/<int:pk>/', AudienceDetailView.as_view(), name='audience-entry'),
    path('audience_create/', AudienceCreateView.as_view(), name='audience-create'),
    path('audience_update/<int:pk>/', AudienceUpdateView.as_view(), name='audience-update'),
    path('audience_delete/<int:pk>/', AudienceDeleteView.as_view(), name='audience-delete'),

    # Mailing List
    path('mailing_list/', MailingListListView.as_view(), name='mailing-list'),
    path('mailing_list/<int:pk>/', MailingListDetailView.as_view(), name='mailing-list-entry'),
    path('mailing_list_create/', MailingListCreateView.as_view(), name='mailing-list-create'),
    path('mailing_list_update/<int:pk>/', MailingListUpdateView.as_view(), name='mailing-list-update'),
    path('mailing_list_delete/<int:pk>/', MailingListDeleteView.as_view(), name='mailing-list-delete'),
    path('mailing_list/unsubscribe/<str:audience>/<str:email>/', unsubscribe, name='unsubscribe'),

    # Email Campaign
    path('email_campaigns/', EmailCampaignListView.as_view(), name='email-campaigns'),
    path('email_campaign/<int:pk>/', EmailCampaignDetailView.as_view(), name='email-campaign-entry'),
    path('email_campaign_create/', EmailCampaignCreateView.as_view(), name='email-campaign-create'),
    path('email_campaign_update/<int:pk>/', EmailCampaignUpdateView.as_view(), name='email-campaign-update'),
    path('email_campaign_delete/<int:pk>/', EmailCampaignDeleteView.as_view(), name='email-campaign-delete'),
]