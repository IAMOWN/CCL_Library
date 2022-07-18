from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Task,
    ServiceGroup,
    LEE,
    PEeP,
    Audience,
    MailingList,
    EmailCampaign,
)
from .forms import (
    CreateTaskForm,
    UpdateTaskForm,
    CreateLibraryTaskForm,
    UpdateLibraryTaskForm,
    CreateServiceGroupForm,
    UpdateServiceGroupForm,
    CreateLEEForm,
    UpdateLEEForm,
    CreatePEePForm,
    UpdatePEePForm,
    CreateAudienceForm,
    UpdateAudienceForm,
    CreateMailingListForm,
    UpdateMailingListForm,
    CreateEmailCampaignForm,
    UpdateEmailCampaignForm,
)

from library.models import (
    LibraryRecord,
    LibraryObservation,
)

from users.models import (
    Profile,
)

# ####################### CONSTANTS #######################
DOMAIN = settings.DOMAIN
UNSUBSCRIBE_URL_EMAIL = 'https://cosmicchrist.love/mailing_list/unsubscribe_email/'
UNSUBSCRIBE_URL_USER = 'https://cosmicchrist.love/mailing_list/unsubscribe_user/'
FROM_EMAIL = 'info@lanesflow.io'
EMAIL_MESSAGE_1 = '''
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                      <head>
                      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                      <title>Whurthy Notification</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    </head>
                    <body style="margin: 0; padding: 0;">
                      <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: none; border-collapse: collapse; font-family:  Arial, sans-serif; font-size: 14px; line-height: 1.5;">
                        <tbody>
                          <tr>
                            <td style="width: 100%;">
                              <div style="text-align: left;">
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Header.png" alt="Soul Synthesis email header banner" width: 600px;"/>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td class="ms-rteTableEvenCol-0" align="left">
                              <div>
                                <p>
                                <span style="color: #000000; background-color: transparent; font-family: arial;">
'''
EMAIL_MESSAGE_CAMPAIGN_1 = '''
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                      <head>
                      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                      <title>Whurthy Notification</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    </head>
                    <body style="margin: 0; padding: 0;">
                      <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: none; border-collapse: collapse; font-family:  Arial, sans-serif; font-size: 14px; line-height: 1.5;">
                        <tbody>
                          <tr>
                            <td style="width: 100%;">
                              <div style="text-align: left;">
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Header%20-%20Campaign.png" alt="Soul Synthesis email header banner" width: 600px;"/>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td class="ms-rteTableEvenCol-0" align="left">
                              <div>
                                <p>
                                <span style="color: #000000; background-color: transparent; font-family: arial;">
'''
EMAIL_MESSAGE_2 = '''
                                </span>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td style="width: 100%;">
                              <div style="text-align: left;">
                                <a href="https://cosmicchrist.love/"><img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Footer.png" alt="Whurthy email header banner" width: 600px;" style="border: 0;" /></a>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </body>
                    </html>
'''

LIBRARY_TASK_URL = 'https://cosmicchrist.love/tasks/library/'
TASKS_URL = 'https://cosmicchrist.love/tasks/'
TASK_URL = 'https://cosmicchrist.love/task/'
EMAIL_CAMPAIGN_URL = 'email_campaign_create/'
EMAIL_CAMPAIGN_DETAIL_URL = 'https://cosmicchrist.love/email_campaign/'

LEE_TASK_RECORD_OBS_2 = 'Record Observation (2) Book File Review'
BOOK_EDITOR_GROUP_NAME = 'Book Editors'

LEE_TASK_CAMPAIGN_3 = 'Email Campaign (3) Accept Test Email'
LEE_TASK_EMAIL_CAMPAIGN_2 = 'Email Campaign Reviewer'
LEE_TASK_CAMPAIGN_4 = 'Email Campaign (4) Review Email'
LEE_TASK_CAMPAIGN_5 = 'Email Campaign (5) Review Revision Comments'

# ####################### FUNCTIONS #######################
def get_current_date():
    return datetime.now().date()

def send_email(subject, to_email, message):
    send_mail(
        subject,
        message,
        FROM_EMAIL,
        [to_email],
        fail_silently=True,
        html_message=message,
    )
    return


# ####################### LEE #######################
class LEEListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """LEE ListView."""
    model = LEE
    template_name = 'iamown/lee.html'
    context_object_name = 'LEE'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dear_souls'] = User.objects.filter(is_staff=True)

        context['search_off'] = True
        search_input = self.request.GET.get('search-area') or ''
        code_search_input = self.request.GET.get('code-search-area') or ''
        owner_search_input = self.request.GET.get('owner-search-area') or ''
        if search_input:
            context['LEE'] = context['LEE'].filter(task_name__icontains=search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = search_input
            context['search_type'] = 'Task'
            context['search_off'] = False
        if code_search_input:
            context['LEE'] = context['LEE'].filter(application__icontains=code_search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = code_search_input
            context['search_type'] = 'App'
            context['search_off'] = False
        if owner_search_input:
            context['LEE'] = context['LEE'].filter(responsible_for_entry__username__icontains=owner_search_input)
            context['search_count'] = context['LEE'].count()
            context['search_entered'] = owner_search_input
            context['search_type'] = 'Owner'
            context['search_off'] = False

        context['search_input'] = search_input

        return context


class LEEDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """LEE DetailView."""
    model = LEE
    template_name = 'iamown/lee_detail.html'
    context_object_name = 'LEE'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LEECreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """LEE CreateView."""
    model = LEE
    form_class = CreateLEEForm

    template_name = 'iamown/lee_form.html'

    success_url = reverse_lazy('lee')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = form.instance.task_name
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The LEE entry "{message}" has been added.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


class LEEUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """LEE entry UpdateView."""
    model = LEE
    form_class = UpdateLEEForm

    template_name = 'iamown/lee_form.html'
    success_url = reverse_lazy('lee')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = form.instance.task_name
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The LEE entry "{message}" has been updated.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['LEE_obj'] = LEE.objects.get(id=self.kwargs['pk'])
        context['page_type'] = 'Update'

        return context


class LEEDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """LEE entry DeleteView."""
    model = LEE
    context_object_name = 'LEE'
    success_url = reverse_lazy('lee')
    template_name = 'iamown/lee_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# ####################### TASK VIEWS #######################
class TaskList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task ListView - Does not include Library Tasks"""
    model = Task
    template_name = 'iamown/tasks.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter().exclude(task_status='Completed').exclude(task_type__in=['Library Observation', 'Book Edit']).order_by(
            'task_status',
            'task_priority',
            'due_date',
        )
        context['tasks'] = tasks
        context['tasks_count'] = tasks.count()
        context['completed_tasks_count'] = Task.objects.filter(
            task_status='Completed'
        ).exclude(task_type__in=['Library Observation', 'Book Edit'],
                  ).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(task_title__icontains=search_input)  # Can also use __startswith
        context['search_input'] = search_input
        context['dear_souls'] = Profile.objects.filter(user__is_staff=True)

        # Search Inputs
        context['search_off'] = True
        assignee_search_input = self.request.GET.get('assignee-search-area') or ''
        task_search_input = self.request.GET.get('task-search-area') or ''
        status_search_input = self.request.GET.get('status-search-area') or ''
        priority_search_input = self.request.GET.get('priority-search-area') or ''

        # Process searches - Dear Soul
        context['search_count'] = 0
        if assignee_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].exclude(task_type__in=['Library Observation', 'Book Edit']).filter(assigned_profile__spiritual_name=assignee_search_input).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Dear Soul'
            context['search_entered'] = assignee_search_input
            context['search_entered'] = assignee_search_input
        # Task Status
        elif status_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].exclude(task_type__in=['Library Observation', 'Book Edit']).filter(task_status__icontains=status_search_input).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Status'
            context['search_entered'] = status_search_input
        # Task Priority
        elif priority_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].exclude(task_type__in=['Library Observation', 'Book Edit']).filter(task_priority__icontains=priority_search_input).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['search_count'] = context['tasks'].exclude(task_status='Completed').count()
            context['search_type'] = 'Priority'
            context['search_entered'] = priority_search_input

        return context


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task DetailView."""
    model = Task
    template_name = 'iamown/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Task CreateView for non-library tasks."""
    model = Task
    form_class = CreateTaskForm

    template_name = 'iamown/task_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        task = form.save()
        task_creator = Profile.objects.get(user__username=self.request.user).spiritual_name
        task.task_history_log = f'''>>> Task manually created by <strong>{task_creator}</strong> on <strong>{get_current_date()}</strong>.<br>Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['page_type'] = 'Create'

        return context


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task UpdateView for non-library tasks."""
    model = Task
    form_class = UpdateTaskForm

    template_name = 'iamown/task_form.html'

    success_url = reverse_lazy('tasks')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_profile'] = self.request.user.profile
        context['page_type'] = 'Update'

        return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task_updater = Profile.objects.get(user__username=self.request.user).spiritual_name
        email_campaign_obj = task.email_campaign
        mailing_list = MailingList.objects.filter(audience=email_campaign_obj.audience)
        print(f'task.task_type: {task.task_type}')

        # "Email Campaign" branch - Test Email
        if task.task_type == 'Email Campaign':
            # AGREE: Test Email accepted
            print('1) EMAIL CAMPAIGN')
            if task.decision == 'Agreed' and task.email_campaign_test_accepted == 'No':
                # Query email campaign
                audience = email_campaign_obj.audience
                subject = email_campaign_obj.subject
                date_sent = email_campaign_obj.date_created
                mailing_list_count = mailing_list.count()

                # Pre-build Email Campaign send log
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Test Email</strong> task marked as <strong>Agreed</strong> by <strong>{email_campaign_obj.sender}</strong> on <strong>{get_current_date()}</strong>.'''

                # Update task
                task.date_completed = get_current_date()
                task.task_status = 'Completed'
                task.actions_taken = task.actions_taken + ' Test Email Accepted'
                task.email_campaign_test_accepted = 'Yes'
                task.task_history_log = task.task_history_log + f'''>>> Test Campaign Email <strong>Accepted</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Date completed: {get_current_date()}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
                task.save(update_fields=[
                    'task_history_log',
                    'date_completed',
                    'task_status',
                    'actions_taken',
                    'email_campaign_test_accepted',
                ])

                # Assign review task to reviews
                reviewers = PEeP.objects.filter(functional_activity=LEE_TASK_EMAIL_CAMPAIGN_2).values_list('dear_soul_responsible')  # Deliberately opted to not code logic for no reviewers!
                reviewer_count = 0
                for id in reviewers:
                    # Create Reviewer Agreement Task and send email
                    reviewer_count += 1
                    reviewer_profile_obj = Profile.objects.get(user_id=id)

                    # Assign Task
                    task_description = LEE.objects.get(task_name=LEE_TASK_CAMPAIGN_4).process_description + f'''<br>Total <strong>number of emails</strong> in Mailing List: <strong>{mailing_list_count}</strong>'''
                    history_log = f'''>>> <strong>Email Campaign Review</strong> task created by {self.request.user.profile.spiritual_name} on <strong>{get_current_date()}</strong><p><br>'''
                    new_task = Task.objects.create(
                        task_title=f'[Review Test Campaign Email] {audience} - {subject} ({date_sent.strftime("%Y-%m-%d")})',
                        task_type='Email Campaign 2',
                        task_description=task_description,
                        task_history_log=history_log,
                        assigned_profile=reviewer_profile_obj,
                        email_campaign=email_campaign_obj,
                    )

                    # Send email for review
                    reviewer_obj = Profile.objects.get(user_id=id)
                    email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Review</strong> sent to <strong>{reviewer_obj.spiritual_name}</strong> on <strong>{get_current_date()}</strong>'''

                    email_address = reviewer_obj.user.email
                    reviewer_name = reviewer_obj.spiritual_name

                    email_subject = f'[CCL] Agreement required for Email Campaign: {email_campaign_obj.subject}'
                    email_campaign_message = email_campaign_obj.message
                    email_message = f"""
                    {EMAIL_MESSAGE_CAMPAIGN_1}
                    *** Beloved {reviewer_name}, this is a CCL ServiceFlow <strong>review email</strong>. Please Qualify readiness to broadcast and update corresponding <a href="{TASK_URL}{new_task.id}/">Task</a>. ***<hr>
                    {email_campaign_message}
                    {EMAIL_MESSAGE_2}
                    """
                    send_email(email_subject, email_address, email_message)

                # Update email campaign object
                email_campaign_obj.send_status = '2) In progress'
                email_campaign_obj.number_of_reviewers = reviewer_count
                email_campaign_obj.review_email_sent = 'Yes'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                    'number_of_reviewers',
                    'review_email_sent',
                ])

            # REVISE: Test Email task marked as 'Revise' -> Resend Email
            if task.decision == 'Revise' and task.email_campaign_test_accepted == 'No':
                # Resend email
                email_address = self.request.user.email
                email_subject = email_campaign_obj.subject
                email_message = f"""
                {EMAIL_MESSAGE_CAMPAIGN_1}
                *** This is a TEST EMAIL (REVISED) * Please make any changes in the <a href="{EMAIL_CAMPAIGN_DETAIL_URL}{email_campaign.id}/">Email Campaign</a>. ***<br>
                *** Once you are satisfied please update this <a href="{TASK_URL}{task_obj.id}">Task</a> as Revise to send another test email, or Agree to continue the ServiceFlow. ***<p>
                {email_campaign_obj.message}
                {EMAIL_MESSAGE_2}
                """
                send_email(email_subject, email_address, email_message)

                # Update email campaign
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email campaign Test Email</strong> task marked as <strong>Revise</strong> by <strong>{email_campaign_obj.sender}</strong> on <strong>{get_current_date()}</strong>.'''
                email_campaign_obj.send_status = '2) In progress'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                ])

                # Update task
                task.task_status = '2) In progress'
                task.actions_taken = task.actions_taken + 'Test Email revision requested'
                task.task_history_log = task.task_history_log + f'''>>> Test Campaign Email marked <strong>Revise</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong> >>> Status: {task.task_status} >>>Priority: {task.task_priority} >>> Due date: {task.due_date}<p>'''
                task.save(update_fields=[
                    'task_status',
                    'task_history_log',
                    'actions_taken',
                ])

            # DECLINE: Test Email task marked as 'Decline' -> End ServiceFlow
            if task.decision == 'Decline' and task.email_campaign_test_accepted == 'No':
                # Update email campaign
                email_campaign.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email campaign Test Email</strong> task marked as <strong>Decline</strong> by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>.'''
                email_campaign_obj.send_status = '4) Declined'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                ])

                # Update task
                task.task_status = 'Completed'
                task.task_history_log = task.task_history_log + f'''>>> Test Campaign Email marked <strong>Decline</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong> >>> Priority: {task.task_priority} >>> Due date: {task.instance.due_date} >>> Assigned Dear Soul: {task_updater}<p>'''
                task.actions_taken = task.actions_taken + '<br>Test Email declined. ServiceFlow ended.'
                task.date_completed = get_current_date()
                task.save(update_fields=[
                    'task_status',
                    'task_history_log',
                    'actions_taken',
                    'date_completed',
                ])

        # "Email Campaign 2" branch - Email Campaign Review emails
        elif task.task_type == 'Email Campaign 2':
            print('2) EMAIL CAMPAIGN')
            number_of_reviewers = email_campaign_obj.number_of_reviewers
            number_of_accepted_reviews = email_campaign_obj.number_of_accepted_reviews
            number_of_declined_reviews = email_campaign_obj.number_of_declined_reviews

            # AGREE: Reviewer Agrees with Email Campaign messaage
            if task.decision == 'Agreed':
                number_of_accepted_reviews += 1

                # Update email campaign object for this Reviewer
                email_campaign_obj.number_of_accepted_reviews = number_of_accepted_reviews
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Review</strong> task marked as <strong>Agreed</strong> by <strong>{task.assigned_profile}</strong> on <strong>{get_current_date()}</strong> >>> Number of Accepted Reviews: {number_of_accepted_reviews}'''
                email_campaign_obj.save(update_fields=[
                    'number_of_accepted_reviews',
                    'email_send_log',
                ])

                # Update task
                task.date_completed = get_current_date()
                task.task_status = 'Completed'
                task.actions_taken = task.actions_taken + 'Email Campaign Accepted'
                task.email_campaign_test_accepted = 'Yes'
                task.task_history_log = task.task_history_log + f'''>>> Test Campaign Email <strong>Accepted</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Date completed: {get_current_date()}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
                task.save(update_fields=[
                    'task_history_log',
                    'date_completed',
                    'task_status',
                    'actions_taken',
                    'email_campaign_test_accepted',
                ])

                # All Reviewers Agree - Send Email Campaign
                if number_of_reviewers == number_of_accepted_reviews:
                    # Update email campaign object marking Agreement
                    email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Agreed ready to send by all reviewers</strong> on <strong>{get_current_date()}</strong> >>> Reviews: <strong>{number_of_accepted_reviews} Agreed/{number_of_reviewers} Reviewers</strong>'''
                    email_campaign_obj.date_published = get_current_date()
                    email_campaign_obj.save(update_fields=[
                        'number_of_accepted_reviews',
                        'date_published',
                        'email_send_log',
                    ])

                    # Send Campaign Email to mailing list
                    email_subject = email_campaign_obj.subject

                    emails_sent = 0
                    for entry in mailing_list:
                        if entry.subscribed == 'Yes':
                            if entry.email:
                                email_address = entry.email
                                unsubscribe_url = f'{UNSUBSCRIBE_URL_EMAIL}{entry.audience}/{email_address}'
                            else:
                                email_address = entry.user.email
                                unsubscribe_url = f'{UNSUBSCRIBE_URL_USER}{entry.audience}/{self.request.user}'
                            # Add unsubscribe link to email message
                            email_message = f'''
                            {EMAIL_MESSAGE_CAMPAIGN_1}
                            {email_campaign_obj.message}
                            <p><center><a href="{unsubscribe_url}">Unsubscribe</a></center><br>
                            {EMAIL_MESSAGE_2}'''
                            send_email(email_subject, email_address, email_message)
                            emails_sent += 1

                    # Update email campaign
                    email_campaign_obj.email_campaign_sent = 'Yes'
                    email_campaign_obj.send_status = 'Sent'
                    email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign SENT</strong> to <strong>{emails_sent}</strong> Dear Souls on <strong>{get_current_date()}</strong>'''
                    email_campaign_obj.save(update_fields=[
                        'email_campaign_sent',
                        'send_status',
                        'email_send_log',
                    ])

                    # Update task
                    task.task_history_log = task.task_history_log + f'''>>> <strong>Email Campaign SENT</strong> on <strong>{get_current_date()}</strong><br><strong>Email Campaign ServiceFlow complete</strong><br>'''
                    task.save(update_fields=[
                        'task_history_log',
                    ])

            # REVISE: Reviewer requests Revision with Email Campaign messaage
            elif task.decision == 'Revise':
                # Update email campaign object for this Reviewer
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Review</strong> task marked as <strong>Revise</strong> by <strong>{task.assigned_profile}</strong> on <strong>{get_current_date()}</strong>'''
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                ])

                # Update current task
                task.date_completed = get_current_date()
                task.task_status = 'Completed'
                task.actions_taken = task.actions_taken + f'Email Campaign - Revisions Requested by <strong>{task.assigned_profile}</strong> (see task history log for comments).<br>'
                task.task_history_log = task.task_history_log + f'''>>> <strong>Revisions requested</strong> for this Test Campaign Email by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Revision Comments:</strong><br>{task.decision_comments}<br><strong>Date completed: {get_current_date()}</strong><p>'''
                task.save(update_fields=[
                    'task_history_log',
                    'date_completed',
                    'task_status',
                    'actions_taken',
                ])

                # Update all remaining incomplete tasks related to this campaign
                incomplete_tasks = Task.objects.filter(email_campaign=email_campaign_obj).exclude(task_status='Completed')
                print(f'incomplete_tasks: {incomplete_tasks}')
                for task_to_update in incomplete_tasks:
                    task_to_update.date_completed = get_current_date()
                    task_to_update.task_status = 'Completed'
                    task_to_update.actions_taken = task_to_update.actions_taken + f'Email Campaign - Revisions Requested by <strong>{task.assigned_profile}</strong> (see task history log for comments).<br>'
                    task_to_update.task_history_log = task_to_update.task_history_log + f'''>>> <strong>Revisions requested</strong> for this Test Campaign Email by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Revision Comments:</strong><br>{task.decision_comments}<br><strong>Date completed: {get_current_date()}</strong><p>'''
                    task_to_update.save(update_fields=[
                        'task_history_log',
                        'date_completed',
                        'task_status',
                        'actions_taken',
                    ])

                # Create new 'Email Campaign 2 - Revise' task
                task_description = LEE.objects.get(task_name=LEE_TASK_CAMPAIGN_5).process_description + f'''<strong>Email Campaign: </strong><a href="{DOMAIN}email_campaign/{email_campaign_obj.id}/" class="text-CCL-Blue" target="_blank">{email_campaign_obj.audience} - {email_campaign_obj.subject} ({email_campaign_obj.date_created.strftime('%Y-%m-%d')})</a><p><br>
                <strong>Reviewer: </strong>{task.assigned_profile}<br>
                <strong>Revision Request: </strong><br>
                {task.decision_comments}
                '''
                history_log = f'''>>> <strong>Campaign Email Revision Request</strong> task created by <strong>{task.assigned_profile}</strong> on <strong>{get_current_date()}</strong><p><br>'''
                task_assignee = Profile.objects.get(spiritual_name=email_campaign_obj.sender)
                new_task = Task.objects.create(
                    task_title=f'[Revise Campaign Email Message] {email_campaign_obj.audience} - {email_campaign_obj.subject}',
                    task_type='Email Campaign',
                    task_description=task_description,
                    task_history_log=history_log,
                    assigned_profile=task_assignee,
                    email_campaign=email_campaign_obj,
                    decision='',
                )

                # Email reviewers letting them know that revision is in progress
                reviewers = PEeP.objects.filter(functional_activity=LEE_TASK_EMAIL_CAMPAIGN_2).values_list('dear_soul_responsible')
                for id in reviewers:
                    reviewer_obj = Profile.objects.get(user_id=id)
                    email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Review UPDATE</strong> sent to <strong>{reviewer_obj.spiritual_name}</strong> on <strong>{get_current_date()}</strong>'''

                    email_address = reviewer_obj.user.email
                    reviewer_name = reviewer_obj.spiritual_name

                    email_subject = f'[CCL] Update - Revisions requested for Email Campaign: {email_campaign_obj.subject}'
                    email_campaign_message = email_campaign_obj.message
                    email_message = f"""
                    {EMAIL_MESSAGE_CAMPAIGN_1}
                    *** Beloved {reviewer_name}, this is a CCL ServiceFlow <strong>review email</strong>. Any uncompleted tasks will be automatically completed and no further review is required until the Sender has completed their task to incorporate the Revision Request and re-initiate a Email Campaign Review. ***<hr>
                    <strong>Reviewer who requested the Revision: </strong>{task.assigned_profile}<br>
                    <strong>Revision Comments:</strong> {task.decision_comments}
                    {EMAIL_MESSAGE_2}
                    """
                    send_email(email_subject, email_address, email_message)

                # Email sender update
                email_address = email_campaign_obj.sender_email
                email_subject = f'[CCL] Update - Revisions requested for Email Campaign: {email_campaign_obj.subject}'
                email_message = f'''
                {EMAIL_MESSAGE_CAMPAIGN_1}
                <strong>Reviewer who requested the Revision: </strong>{task.assigned_profile}<br>
                <strong>Revision Comments:</strong> {task.decision_comments}<p>
                *** Please check the <a href="{TASK_URL}{new_task.id}">Task</a> to review these comments and update the Email Campaign ***<p>
                {EMAIL_MESSAGE_2}
                '''
                send_email(email_subject, email_address, email_message)

            # DECLINE: Reviewer Declines Email Campaign messaage
            elif task.decision == 'Decline':
                number_of_declined_reviews += 1

                # Update email campaign object for this Reviewer
                email_campaign_obj.number_of_declined_reviews = number_of_declined_reviews
                email_campaign_obj.send_status = '4) Declined'
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Declined</strong> by <strong>{task.assigned_profile}</strong> on <strong>{get_current_date()}</strong>'''
                email_campaign_obj.save(update_fields=[
                    'send_status',
                    'number_of_declined_reviews',
                    'email_send_log',
                ])

                # Update all incomplete tasks related to this campaign
                incomplete_tasks = Task.objects.filter(email_campaign=email_campaign_obj).exclude(task_status='Completed')
                for task_to_update in incomplete_tasks:
                    task_to_update.date_completed = get_current_date()
                    task_to_update.task_status = 'Completed'
                    task_to_update.actions_taken = task_to_update.actions_taken + f'Email Campaign Declined by <strong>{task.assigned_profile}</strong> (see task history log for comments).<br>'
                    task_to_update.task_history_log = task_to_update.task_history_log + f'''>>> <strong>Campaign Email Declined</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Date completed: {get_current_date()}</strong><p>'''
                    task_to_update.save(update_fields=[
                        'task_history_log',
                        'date_completed',
                        'task_status',
                        'actions_taken',
                    ])

                # Email sender update
                email_address = email_campaign_obj.sender.user.email
                email_subject = f'[CCL] Update - Email Campaign Declined: {email_campaign_obj.subject}'
                email_message = f'''
                {EMAIL_MESSAGE_CAMPAIGN_1}
                <strong>Reviewer: </strong>{task.assigned_profile}<br>
                <strong>Revision Comments:</strong> {task.decision_comments}<p>
                *** This ServiceFlow has ended. If you wish to continue then you can create a new <a href="{DOMAIN}{EMAIL_CAMPAIGN_URL}">Email Campaign</a>. ***<p>
                {EMAIL_MESSAGE_2}
                '''
                send_email(email_subject, email_address, email_message)  # ServiceFlow END

        # 'Email Campaign - 2 - Revise' Branch
        elif task.task_type == 'Email Campaign - 2 - Revise':
            # AGREE: Sender has made changes. Reviewer tasks will be created
            print('2) EMAIL CAMPAIGN - Revise')
            if task.decision == 'Agreed':
                # Query email campaign
                audience = email_campaign_obj.audience
                subject = email_campaign_obj.subject
                date_sent = email_campaign_obj.date_created
                mailing_list_count = mailing_list.count()

                # Pre-build Email Campaign send log
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign REVISION Email</strong> task marked as <strong>Agreed</strong> by <strong>{email_campaign_obj.sender}</strong> on <strong>{get_current_date()}</strong>.'''

                # Update task
                task.date_completed = get_current_date()
                task.task_status = 'Completed'
                task.actions_taken = task.actions_taken + ' REVISION Email Accepted'
                task.email_campaign_test_accepted = 'Yes'
                task.task_history_log = task.task_history_log + f'''>>> REVISED Campaign Email <strong>Accepted</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Date completed: {get_current_date()}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
                task.save(update_fields=[
                    'task_history_log',
                    'date_completed',
                    'task_status',
                    'actions_taken',
                    'email_campaign_test_accepted',
                ])

                # Assign review task to reviews
                reviewers = PEeP.objects.filter(functional_activity=LEE_TASK_EMAIL_CAMPAIGN_2).values_list('dear_soul_responsible')  # Deliberately opted to not code logic for no reviewers!
                reviewer_count = 0
                for id in reviewers:
                    # Create Reviewer Agreement Task and send email
                    reviewer_count += 1
                    reviewer_profile_obj = Profile.objects.get(user_id=id)

                    # Assign Task
                    task_description = LEE.objects.get(task_name=LEE_TASK_CAMPAIGN_4).process_description + f'''<br>Total <strong>number of emails</strong> in Mailing List: <strong>{mailing_list_count}</strong>'''
                    history_log = f'''>>> <strong>Email Campaign Review</strong> task created by {self.request.user.profile.spiritual_name} on <strong>{get_current_date()}</strong><p><br>'''
                    new_task = Task.objects.create(
                        task_title=f'[Review Test Campaign Email] {audience} - {subject} ({date_sent.strftime("%Y-%m-%d")})',
                        task_type='Email Campaign 2',
                        task_description=task_description,
                        task_history_log=history_log,
                        assigned_profile=reviewer_profile_obj,
                        email_campaign=email_campaign_obj,
                    )

                    # Send email for review
                    reviewer_obj = Profile.objects.get(user_id=id)
                    email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email Campaign Review</strong> sent to <strong>{reviewer_obj.spiritual_name}</strong> on <strong>{get_current_date()}</strong>'''

                    email_address = reviewer_obj.user.email
                    reviewer_name = reviewer_obj.spiritual_name

                    email_subject = f'[CCL] Agreement required for Email Campaign: {email_campaign_obj.subject}'
                    email_campaign_message = email_campaign_obj.message
                    email_message = f"""
                    {EMAIL_MESSAGE_CAMPAIGN_1}
                    *** Beloved {reviewer_name}, this is a CCL ServiceFlow <strong>review email</strong>. Please Qualify readiness to broadcast and update corresponding <a href="{TASK_URL}{new_task.id}/">Task</a>. ***<hr>
                    {email_campaign_message}
                    {EMAIL_MESSAGE_2}
                    """
                    send_email(email_subject, email_address, email_message)

                # Update email campaign object
                email_campaign_obj.send_status = '2) In progress'
                email_campaign_obj.number_of_reviewers = reviewer_count
                email_campaign_obj.review_email_sent = 'Yes'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                    'number_of_reviewers',
                    'review_email_sent',
                ])

            # REVISE: Sender wants to review their changes in an email
            elif task.decision == 'Revise':
                # Resend email
                email_address = self.request.user.email
                email_subject = email_campaign_obj.subject
                email_message = f"""
                {EMAIL_MESSAGE_CAMPAIGN_1}
                *** This is a TEST EMAIL (REVISED) * Please make any changes in the <a href="{EMAIL_CAMPAIGN_DETAIL_URL}{email_campaign.id}/">Email Campaign</a>. ***<br>
                *** Once you are satisfied please update this <a href="{TASK_URL}{task_obj.id}">Task</a> as Revise to send another test email, or Agree to continue the ServiceFlow. ***<p>
                {email_campaign_obj.message}
                {EMAIL_MESSAGE_2}
                """
                send_email(email_subject, email_address, email_message)

                # Update email campaign
                email_campaign_obj.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email campaign REVISION Email</strong> task marked as <strong>Revise</strong> by <strong>{email_campaign_obj.sender}</strong> on <strong>{get_current_date()}</strong>.'''
                email_campaign_obj.send_status = '2) In progress'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                ])

                # Update task
                task.task_status = '2) In progress'
                task.actions_taken = task.actions_taken + '<br>REVISION Email revision requested'
                task.task_history_log = task.task_history_log + f'''>>> REVISION Campaign Email marked <strong>Revise</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong> >>> Status: {task.task_status} >>>Priority: {task.task_priority} >>> Due date: {task.due_date}<p>'''
                task.save(update_fields=[
                    'task_status',
                    'task_history_log',
                    'actions_taken',
                ])

            # DECLINE: Sender wants to end the ServiceFlow
            elif task.decision == 'Decine':
                # Update email campaign
                email_campaign.email_send_log = email_campaign_obj.email_send_log + f'''<br>>>> <strong>Email campaign REVISION Email</strong> task marked as <strong>Decline</strong> by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>.'''
                email_campaign_obj.send_status = '4) Declined'
                email_campaign_obj.save(update_fields=[
                    'email_send_log',
                    'send_status',
                ])

                # Update task
                task.task_status = 'Completed'
                task.task_history_log = task.task_history_log + f'''>>> REVISION Campaign Email marked <strong>Decline</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong> >>> Priority: {task.task_priority} >>> Due date: {task.instance.due_date} >>> Assigned Dear Soul: {task_updater}<p>'''
                task.actions_taken = task.actions_taken + '<br>Test Email declined. ServiceFlow ended.'
                task.date_completed = get_current_date()
                task.save(update_fields=[
                    'task_status',
                    'task_history_log',
                    'actions_taken',
                    'date_completed',
                ])

            # Task updated without change to Decision
            else:
                task.task_history_log = task.task_history_log + f'''>>> Task manually <strong>updated</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
                task.save(update_fields=['task_history_log',])

        # (General) Task marked complete
        elif task.task_status == 'Completed':
            print('COMPLETE')
            if task.actions_taken == "":
                form.add_error(
                    'actions_taken',
                    'Please enter the actions taken as a part of completing this task.'
                )
                return self.form_invalid(form)
            task.date_completed = get_current_date()
            task.task_history_log = task.task_history_log + f'''>>> Task manually <strong>completed</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br><strong>Date completed: {get_current_date()}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
            task.save(update_fields=['task_history_log','date_completed',])

        # (General) Task updated
        else:
            print('ELSE')
            task.task_history_log = task.task_history_log + f'''>>> Task manually <strong>updated</strong> by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile}<p>'''
            task.save(update_fields=['task_history_log',])

        if task.task_type == 'Email Campaign 2' and task.decision == 'Agreed':
            message = form.instance.task_title + f' and Email Campaign Reviews have been sent to Reviewers'
        else:
            message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been updated'
        )
        return super().form_valid(form)


class TaskCompletedList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task ListView for non-library completed tasks."""
    model = Task
    template_name = 'iamown/tasks_completed.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_tasks = Task.objects.all().filter(
            task_status='Completed',
        ).exclude(task_type__in=['Library Observation', 'Book Edit'])
        context['tasks'] = completed_tasks
        context['completed_tasks_count'] = completed_tasks.count()
        context['tasks_count'] = Task.objects.all().\
            exclude(task_status='Completed').\
            exclude(task_type__in=['Library Observation', 'Book Edit']).count()
        context['title'] = 'Completed Tasks'

        return context


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Task DeleteView for non-library tasks."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'iamown/task_confirm_delete.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# ####################### LIBRARY TASK VIEWS #######################
class TaskLibraryList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Library Task ListView."""
    model = Task
    template_name = 'iamown/tasks_library.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter().filter(
            task_type__in=['Library Observation', 'Book Edit']
        ).exclude(task_status='Completed').order_by(
            'task_status',
            'task_priority',
            'due_date',
        )
        # TODO Check tasks count on tasks library template
        context['tasks'] = tasks
        context['tasks_count'] = tasks.count()
        context['completed_tasks_count'] = Task.objects.filter(
            task_type__in=['Library Observation', 'Book Edit'],
            task_status='Completed',
        ).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(task_title__icontains=search_input)
        context['search_input'] = search_input

        context['dear_souls'] = Profile.objects.filter(user__is_staff=True)

        # Search Inputs
        context['search_off'] = True
        assignee_search_input = self.request.GET.get('assignee-search-area') or ''
        status_search_input = self.request.GET.get('status-search-area') or ''
        priority_search_input = self.request.GET.get('priority-search-area') or ''

        # Process searches - Dear Soul
        context['search_count'] = 0
        if assignee_search_input:
            context['search_off'] = False
            search_result = Task.objects.filter(assigned_profile__spiritual_name=assignee_search_input, task_type__in=['Library Observation', 'Book Edit']).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['tasks'] = search_result
            context['search_count'] = search_result.count()
            context['search_type'] = 'Dear Soul'
            context['search_entered'] = assignee_search_input
        # Task Status
        elif status_search_input:
            context['search_off'] = False
            search_result = Task.objects.filter(task_status__icontains=status_search_input, task_type__in=['Library Observation', 'Book Edit']).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['tasks'] = search_result
            context['search_count'] = search_result.count()
            context['search_type'] = 'Status'
            context['search_entered'] = status_search_input
        # Task Priority
        elif priority_search_input:
            context['search_off'] = False
            search_result = Task.objects.filter(task_priority__icontains=priority_search_input, task_type__in=['Library Observation', 'Book Edit']).order_by(
                'task_status',
                'task_priority',
                'due_date',
            )
            context['tasks'] = search_result
            context['search_count'] = search_result.count()
            context['search_type'] = 'Priority'
            context['search_entered'] = priority_search_input

        context['title'] = 'Library Tasks'

        return context


class TaskLibraryDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Library Task DetailView."""
    model = Task
    template_name = 'iamown/task_detail_library.html'
    context_object_name = 'task'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TaskLibraryCompletedList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Completed Library Tasks."""
    model = Task
    template_name = 'iamown/tasks_completed_library.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        tasks = Task.objects.all().filter(
            task_type__in=['Library Observation', 'Book Edit'],
            task_status='Completed',
        ).order_by(
            '-due_date',
        )
        context['tasks'] = tasks
        context['completed_tasks_count'] = tasks.count()
        context['active_tasks_count'] = Task.objects.filter(
            task_type='Library Observation',
        ).exclude(task_status='Completed').count()
        context['title'] = 'Completed Library Tasks'

        return context


class TaskLibraryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Library Task CreateView."""
    model = Task
    form_class = CreateLibraryTaskForm

    template_name = 'iamown/task_form_library.html'

    success_url = reverse_lazy('tasks-library')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        library_task = form.save()
        service_group = ServiceGroup.objects.get(service_group='Digital Librarians')
        library_task.assigned_service_group = service_group
        library_task.task_type = 'Library Observation'
        task_creator = Profile.objects.get(user__username=self.request.user).spiritual_name
        library_task.task_history_log = f'''>>> <strong>Library Observation</strong> >>> Manually created by <strong>{task_creator}</strong><br>
        Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p><br>'''

        library_task.save(update_fields=['task_type', 'task_history_log',])
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Library Observation Task "{message}" has been created'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


class TaskLibraryUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Library Task UpdateView."""
    model = Task
    form_class = UpdateLibraryTaskForm

    template_name = 'iamown/task_form_library.html'

    success_url = reverse_lazy('tasks-library')

    def test_func(self):
        # task = self.get_object()
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context

    def form_valid(self, form):
        library_task = form.save(commit=False)
        if form.instance.task_status == 'Completed':
            if form.instance.book_text_impacted == 'Yes':
                if library_task.actions_taken == "":
                    form.add_error(
                        'actions_taken',
                        'Please enter the actions taken as a part of completing this task.'
                    )
                    return self.form_invalid(form)
                library_task.date_completed = get_current_date()
                library_task.task_history_log = library_task.task_history_log + f'''>>> Task type: <strong>{form.instance.task_type}</strong> manually updated by <strong>{library_task.assigned_profile}</strong> on <strong>{get_current_date()}</strong>.<br>
                Date completed: <strong>{library_task.date_completed}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p>
                '''
                library_task.save(update_fields=['task_history_log','date_completed',])

                service_group = ServiceGroup.objects.get(service_group='Book Editors')
                related_task = Task.objects.get(id=self.kwargs['pk'])

                history_log = f'''>>> <strong>{LEE_TASK_RECORD_OBS_2}</strong> task created from completed Library Observation task: {related_task.task_title}<p><br>'''
                task_description = LEE.objects.get(task_name=LEE_TASK_RECORD_OBS_2).process_description
                if library_task.book_urls_for_record:
                    task_description = task_description + f'''<strong>Book urls:</strong><br>
                    {library_task.book_urls_for_record}
                '''
                else:
                    task_description = task_description + '<strong>There are no book urls listed for this record.</strong>'

                created_task = Task.objects.create(
                    task_title=f'{LEE_TASK_RECORD_OBS_2} Check Book Files related to Library Observation',
                    task_type='Book Edit',
                    task_description=task_description,
                    task_history_log=history_log,
                    assigned_service_group=service_group,
                    related_task=related_task,
                    library_record=library_task.library_record,
                    library_task_description=library_task.task_description,
                    library_task_actions_taken=library_task.actions_taken,
                )
                created_task.save()

                book_editors = User.objects.filter(groups__name=BOOK_EDITOR_GROUP_NAME)
                for editor in book_editors:
                    if editor.profile.notification_preference == 'Email':
                        email_address = editor.email
                        email_subject = '[CCL] A corrected Library observation has been marked as having an impact on book text.'
                        email_message = f"""
                        {EMAIL_MESSAGE_1}
                        Beloved {editor.profile.spiritual_name},<p>
                        A Library Observation has just been completed, and has been marked as having an impact on book text 
                        related to the Library record.<p> 
                        Please review the <a href='{LIBRARY_TASKS_URL}'>Library Tasks</a> at your earliest convenience.<p>
                        Note: It is possible that another Book Editor may respond to this task before you do. When 
                        reviewing the task be sure check the task status as well as the Assigned Dear Soul for the task.<p>
                        Love and Blessings
                        {EMAIL_MESSAGE_2}
                        """
                        send_email(email_subject, email_address, email_message)

            else:
                if library_task.actions_taken == "":
                    form.add_error(
                        'actions_taken',
                        'Please enter the actions taken as a part of completing this task.'
                    )
                    return self.form_invalid(form)

                library_task.date_completed = get_current_date()
                library_task.task_history_log = library_task.task_history_log + f'''>>> Task type: <strong>{form.instance.task_type}</strong> manually updated by <strong>{library_task.assigned_profile}</strong> on <strong>{get_current_date()}</strong>.<br>
                Date completed: <strong>{library_task.date_completed}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p>
                '''

            library_task.save(update_fields=['task_history_log','date_completed',])

        else:
            library_task.task_history_log = library_task.task_history_log + f'''>>> Task type: <strong>{form.instance.task_type}</strong> manually updated by <strong>{library_task.assigned_profile}</strong> on <strong>{get_current_date()}</strong>.<br>
            Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p>
            '''
            library_task.save(update_fields=['task_history_log',])


        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been updated'  # TODO Add if-else for "Email Camp sent..."
        )
        return super().form_valid(form)


class TaskLibraryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Library Task DeleteView."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks-library')
    template_name = 'iamown/task_confirm_delete_library.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Library Observation Task'

        return context


# ####################### SERVICE GROUP VIEWS #######################
class ServiceGroupList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ServiceGroup
    template_name = 'iamown/service_groups.html'
    context_object_name = 'service_groups'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Service Groups'

        return context


class ServiceGroupDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ServiceGroup
    template_name = 'iamown/service_group_detail.html'
    context_object_name = 'service_group'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"EGA Service Group: {ServiceGroup.objects.get(pk=self.kwargs['pk'])}"

        service_group = ServiceGroup.objects.get(id=self.kwargs['pk'])
        # service_group_objectives = Objective.objects\
        #     .filter(service_group=service_group)\
        #     .exclude(objective_status='3) Complete')\
        #     .exclude(objective_status='Cancelled')
        # context['objectives'] = service_group_objectives

        return context


class ServiceGroupCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ServiceGroup
    form_class = CreateServiceGroupForm
    template_name = 'iamown/service_group_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.service_group
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Service Group "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


class ServiceGroupUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceGroup
    form_class = UpdateServiceGroupForm
    template_name = 'iamown/service_group_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.service_group
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Service Group "{message}" has been updated'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


class ServiceGroupDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceGroup
    template_name = 'iamown/service_group_confirm_delete.html'
    success_url = reverse_lazy('service-groups')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# ####################### PEeP #######################
class PEePListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """PEeP ListView."""
    model = PEeP
    template_name = 'iamown/peeps.html'
    context_object_name = 'peeps'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dear_souls'] = User.objects.filter(is_staff=True)
        context['service_groups'] = ServiceGroup.objects.all()

        context['search_off'] = True
        search_input = self.request.GET.get('search-area') or ''
        resp_search_input = self.request.GET.get('resp-search-area') or ''
        group_search_input = self.request.GET.get('group-search-area') or ''
        if search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(functional_activity__icontains=search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = search_input
            context['search_type'] = 'Function'
        if resp_search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(dear_soul_responsible__username__icontains=resp_search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = resp_search_input
            context['search_type'] = 'Resp'
        if group_search_input:
            context['search_off'] = False
            context['peeps'] = context['peeps'].filter(service_group__service_group=group_search_input)
            context['search_count'] = context['peeps'].count()
            context['search_entered'] = group_search_input
            context['search_type'] = 'Group'
        context['search_input'] = search_input

        return context


class PEePDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """PEeP DetailView."""
    model = PEeP
    template_name = 'iamown/peep_detail.html'
    context_object_name = 'peep'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class PEePCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """PEeP CreateView."""
    model = PEeP
    form_class = CreatePEePForm

    template_name = 'iamown/peep_form.html'

    success_url = reverse_lazy('peeps')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = form.instance.functional_activity
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The PEeP entry "{message}" has been added.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


class PEePUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """PEeP entry UpdateView."""
    model = PEeP
    form_class = UpdatePEePForm

    template_name = 'iamown/peep_form.html'
    success_url = reverse_lazy('peeps')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = form.instance.functional_activity
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The PEeP entry "{message}" has been updated.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


class PEePDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """PEeP entry DeleteView."""
    model = PEeP
    context_object_name = 'peep'
    success_url = reverse_lazy('peeps')
    template_name = 'iamown/peep_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# ####################### Audiences #######################
class AudienceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Audience ListView."""
    model = Audience
    template_name = 'iamown/audiences.html'
    context_object_name = 'audiences'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AudienceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Audience DetailView."""
    model = Audience
    template_name = 'iamown/audience_detail.html'
    context_object_name = 'audience'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audience_count'] = MailingList.objects.filter(audience=self.kwargs['pk']).count()

        return context


class AudienceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Audience CreateView."""
    model = Audience
    form_class = CreateAudienceForm

    template_name = 'iamown/audience_form.html'

    success_url = reverse_lazy('audiences')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.ordering = int(Audience.objects.all().count()) + 1
        message = form.instance.audience
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The audience "{message}" has been added.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'
        return context


class AudienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Audience UpdateView."""
    model = Audience
    form_class = UpdateAudienceForm

    template_name = 'iamown/audience_form.html'
    success_url = reverse_lazy('audiences')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = form.instance.audience
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The audience "{message}" has been updated.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'
        return context


class AudienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Audience DeleteView."""
    model = Audience
    context_object_name = 'audience'
    success_url = reverse_lazy('audiences')
    template_name = 'iamown/audience_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# ####################### Mailing List #######################
class MailingListListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """MailingList ListView."""
    model = MailingList
    template_name = 'iamown/mailing_list.html'
    context_object_name = 'mailing_list'
    ordering = 'audience'
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_list_count'] = MailingList.objects.filter(subscribed='Yes').count()

        return context


class MailingListDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """MailingList DetailView."""
    model = MailingList
    template_name = 'iamown/mailing_list_detail.html'
    context_object_name = 'mailing_list_entry'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        entry_obj = MailingList.objects.get(id=self.kwargs['pk'])
        if entry_obj.user:
            context['title'] = f'Mailing List Entry: {entry_obj.user.profile.spiritual_name}'
        else:
            context['title'] = f'Mailing List Entry: {entry_obj.email}'
        return context


class MailingListCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """MailingList CreateView."""
    model = MailingList
    form_class = CreateMailingListForm

    template_name = 'iamown/mailing_list_form.html'

    success_url = reverse_lazy('mailing-list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):  # TODO Refactor form logic in views.py to forms.py
        # Check that the email is not already in the mailing list for this audience
        if form.instance.email:
            mailing_list_email = MailingList.objects.filter(email=form.instance.email, audience=form.instance.audience)
            if not mailing_list_email.exists():
                try:
                    user_email = User.objects.get(email=form.instance.email)
                    form.add_error(
                        'email',
                        f'This email is already associated with the user account, "{user_email.username}". Please enter another email address or select this Dear Soul in the User field.'
                    )
                    return self.form_invalid(form)
                except User.DoesNotExist:
                    message = f'{form.instance.audience}: {form.instance.email}'
                    messages.add_message(
                        self.request,
                        messages.SUCCESS,
                        f'The mailing list entry, "{message}" has been added.'
                    )
                    # return super().form_valid(form)
            else:
                form.add_error(
                    'email',
                    f'This email is already registered for the "{form.instance.audience}" audience.'
                )
                return self.form_invalid(form)
        # Check that the user is not already in the mailing list for this audience
        else:
            mailing_list_user = MailingList.objects.filter(user=form.instance.user, audience=form.instance.audience)
            # if mailing_list_user.count() == 0:
            if not mailing_list_user.exists():
                message = f'{form.instance.audience}: {form.instance.user}'
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    f'The mailing list entry, "{message}" has been added.'
                )
                # return super().form_valid(form)
            else:
                form.add_error(
                    'user',
                    f'The user "{form.instance.user}" is already registered for the "{form.instance.audience}" audience.'
                )
                return self.form_invalid(form)

        entry = form.save()
        entry.mailing_list_log = f'>>> <strong>Record added</strong> by <strong>{self.request.user}</strong> on <strong>{get_current_date()}</strong> >>> Subscribed: <strong>{form.instance.subscribed}</strong>'
        entry.save(update_fields=['mailing_list_log',])

        if form.instance.user:
            message = f'{form.instance.audience} - {form.instance.user} ({get_current_date()})'
        else:
            message = f'{form.instance.audience} - {form.instance.email} ({get_current_date()})'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Mailing List entry "{message}" has been added.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'
        return context


class MailingListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """MailingList UpdateView."""
    model = MailingList
    form_class = UpdateMailingListForm

    template_name = 'iamown/mailing_list_form.html'
    success_url = reverse_lazy('mailing-list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):

        if form.instance.user:
            message = f'{form.instance.audience} - {form.instance.user} ({get_current_date()})'
        else:
            message = f'{form.instance.audience} - {form.instance.email} ({get_current_date()})'

        entry = form.save(commit=False)
        entry.mailing_list_log = entry.mailing_list_log + f'<br>>>> <strong>Record updated</strong> by <strong>{self.request.user}</strong> on <strong>{get_current_date()}</strong> >>> Subscribed: <strong>{form.instance.subscribed}</strong>'
        entry.save(update_fields=['mailing_list_log',])

        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The mailing list entry, "{message}" has been updated.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'
        return context


class MailingListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """MailingList DeleteView."""
    model = MailingList
    context_object_name = 'mailing_list_entry'
    success_url = reverse_lazy('mailing-list')
    template_name = 'iamown/mailing_list_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def unsubscribe_email(request, audience, email):
    mailing_list_record_to_unsubscribe = MailingList.objects.filter(audience__audience=audience, email=email)
    if mailing_list_record_to_unsubscribe.exists():
        for record in mailing_list_record_to_unsubscribe:
            if record.subscribed == 'Yes':
                mailing_list_obj = MailingList.objects.get(id=record.id)
                mailing_list_obj.subscribed = 'No'
                mailing_list_obj.mailing_list_log = mailing_list_obj.mailing_list_log +  f'<br>>>> <strong>Record UNSUBSCRIBED</strong> on <strong>{get_current_date()}</strong> >>> Subscribed: <strong>{mailing_list_obj.subscribed}</strong>'
                mailing_list_obj.save(update_fields=['subscribed', 'mailing_list_log',])
                unsub_message = f'You have successfully unsubscribed the email "{email}" from the "{audience}" mailing list.'
            if record.subscribed == 'No':
                unsub_message = f'The email "{email}" is already unsubscribed from the "{audience}" mailing list.'
    else:
        unsub_message = f'There is no record for the email "{email}" in the "{audience}" mailing list.'

    context = {
        'title': f'Unsubscribe your email from the "{audience}" Mailing List',
        'unsub_message': unsub_message,
    }

    return render(request, 'iamown/unsubscribe.html', context)



def unsubscribe_user(request, audience, user):  # TODO ServiceFlow to follow up with unsubscribes from users?
    mailing_list_record_to_unsubscribe = MailingList.objects.filter(audience__audience=audience, user__username=user)
    if mailing_list_record_to_unsubscribe.exists():
        for record in mailing_list_record_to_unsubscribe:
            if record.subscribed == 'Yes':
                mailing_list_obj = MailingList.objects.get(id=record.id)
                mailing_list_obj.subscribed = 'No'
                mailing_list_obj.mailing_list_log = mailing_list_obj.mailing_list_log +  f'<br>>>> <strong>Record UNSUBSCRIBED</strong> on <strong>{get_current_date()}</strong> >>> Subscribed: <strong>{mailing_list_obj.subscribed}</strong>'
                mailing_list_obj.save(update_fields=['subscribed', 'mailing_list_log',])
                unsub_message = f'You have successfully unsubscribed the user account "{user}" from the "{audience}" mailing list.'
            if record.subscribed == 'No':
                unsub_message = f'The user account "{user}" is already unsubscribed from the "{audience}" mailing list.'
    else:
        unsub_message = f'There is no record for the user account "{user}" in the "{audience}" mailing list.'

    context = {
        'title': f'Unsubscribe your user account from the "{audience}" Mailing List',
        'unsub_message': unsub_message,
    }

    return render(request, 'iamown/unsubscribe.html', context)


@login_required
def bulk_email_import(request):
    if request.method == 'POST':
        audience = request.POST['audience']
        message = request.POST['email-address-import']

        print(f'message: {message}')
        print(f'audience: {audience}')

        context = {
            'title': 'Bulk Email Import',
            'audiences': Audience.objects.all(),
        }

        return render(request, 'home/bulk_email_import.html', context)

    else:
        context = {
            'title': 'Bulk Email Import',
            'audiences': Audience.objects.all()
        }
        return render(request, 'home/bulk_email_import.html', context)


# ####################### Email Campaign #######################
class EmailCampaignListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """EmailCampaign ListView."""
    model = EmailCampaign
    template_name = 'iamown/email_campaigns.html'
    context_object_name = 'email_campaigns'
    ordering = 'audience'
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmailCampaignDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """EmailCampaign DetailView."""
    model = EmailCampaign
    template_name = 'iamown/email_campaign_detail.html'
    context_object_name = 'email_campaign'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        email_campaign_obj = EmailCampaign.objects.get(id=self.kwargs['pk'])
        mailing_list_count = MailingList.objects.filter(audience__audience=email_campaign_obj.audience).count()

        context['title'] = f'Email campaign: {email_campaign_obj.audience} - {email_campaign_obj.subject}'
        context['mailing_list_count'] = mailing_list_count
        return context


class EmailCampaignCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """EmailCampaign CreateView."""
    model = EmailCampaign
    form_class = CreateEmailCampaignForm

    template_name = 'iamown/email_campaign_form.html'

    success_url = reverse_lazy('email-campaigns')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.sender_email = self.request.user.email
        mailing_list_count = MailingList.objects.filter(audience=form.instance.audience).count()
        if mailing_list_count == 0:
            form.add_error(
                'audience',
                'There are no mailing list entries for this Audience. Please select another Audience.'
            )
            return self.form_invalid(form)
        email_campaign = form.save()

        if email_campaign.ready_to_send == 'Yes':
            # Update Email Campaign - ready to send a test email
            if email_campaign.email_send_log is None:
                email_campaign.email_send_log = f'''>>> <strong>Email campaign</strong> created by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>. <strong>Ready to send: {form.instance.ready_to_send}</strong>'''
            else:
                email_campaign.email_send_log = email_campaign.email_send_log + f'''<br>>>> <strong>Email campaign</strong> created by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>. <strong>Ready to send: {form.instance.ready_to_send}</strong>'''
            email_campaign.test_email_sent = 'Yes'
            email_campaign.save(update_fields=[
                'email_send_log',
                'test_email_sent',
            ])

            # Update Task
            task_description = LEE.objects.get(task_name=LEE_TASK_CAMPAIGN_3).process_description + f'''<strong>Email Campaign: </strong><a href="{DOMAIN}email_campaign/{email_campaign.id}/" class="text-CCL-Blue" target="_blank">{email_campaign.audience} - {email_campaign.subject} ({email_campaign.date_created.strftime('%Y-%m-%d')})</a><br>'''
            history_log = f'''>>> <strong>Accept Test Campaign Email</strong> task created by {self.request.user.profile.spiritual_name} on <strong>{get_current_date()}</strong><p><br>'''
            task_obj = Task.objects.create(
                task_title=f'[Accept Test Campaign Email] {form.instance.audience} - {form.instance.subject}',
                task_type='Email Campaign',
                task_description=task_description,
                task_history_log=history_log,
                assigned_profile=self.request.user.profile,
                email_campaign=email_campaign,
            )

            # Send Email
            email_address = self.request.user.email
            email_subject = form.instance.subject
            email_message = f"""
            {EMAIL_MESSAGE_CAMPAIGN_1}
            *** This is a TEST EMAIL * Please make any changes in the <a href="{EMAIL_CAMPAIGN_DETAIL_URL}{email_campaign.id}/">Email Campaign</a>. ***<br>
            *** Once you are satisfied please update this <a href="{TASK_URL}{task_obj.id}">Task</a> as Revise to send another test email, or Agree to continue the ServiceFlow. ***<p>
            {form.instance.message}
            {EMAIL_MESSAGE_2}
            """
            send_email(email_subject, email_address, email_message)
        else:
            # Update Email Campaign - not ready to send a test email
            if email_campaign.email_send_log is None:
                email_campaign.email_send_log = f'''>>> <strong>Email campaign</strong> created by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>. <strong>Ready to send: {form.instance.ready_to_send}</strong>'''
            else:
                email_campaign.email_send_log = email_campaign.email_send_log + f'''<br>>>> <strong>Email campaign</strong> created by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>. <strong>Ready to send: {form.instance.ready_to_send}</strong>'''
            email_campaign.save(update_fields=[
                'email_send_log',
            ])

        message = f'{form.instance.audience} - {form.instance.subject}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The email campaign ServiceFlow for the email, "{message}" has been started. Check your inbox for a test email..'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['form_instructions'] = LEE.objects.get(task_name='Email Campaign (1) Start').process_description
        return context


class EmailCampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """EmailCampaign UpdateView."""
    model = EmailCampaign
    form_class = UpdateEmailCampaignForm

    template_name = 'iamown/email_campaign_form.html'
    success_url = reverse_lazy('email-campaigns')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        email_campaign = form.save()

        mailing_list_count = MailingList.objects.filter(audience=form.instance.audience).count()
        if mailing_list_count == 0:
            form.add_error(
                'audience',
                'There are no mailing list entries for this Audience. Please select another Audience.'
            )
            return self.form_invalid(form)
        if email_campaign.ready_to_send == 'Yes' and email_campaign.test_email_sent == 'No':

            # Update Email Campaign
            email_campaign.email_send_log = email_campaign.email_send_log + f'''<br>>>> <strong>Email Campaign</strong> updated by <strong>{form.instance.sender}</strong> on <strong>{get_current_date()}</strong>. <strong>Ready to send: {form.instance.ready_to_send}</strong>'''
            email_campaign.test_email_sent = 'Yes'
            email_campaign.save(update_fields=[
                'email_send_log',
                'test_email_sent',
            ])

            # Update Task
            task_description = LEE.objects.get(task_name=LEE_TASK_CAMPAIGN_3).process_description + f'''<strong>Email Campaign: </strong><a href="{DOMAIN}email_campaign/{email_campaign.id}/" class="text-CCL-Blue" target="_blank">{email_campaign.audience} - {email_campaign.subject} ({email_campaign.date_created.strftime('%Y-%m-%d')})</a><br>
            '''
            history_log = f'''>>> <strong>Accept Test Campaign Email</strong> task created by {self.request.user.profile.spiritual_name} on <strong>{get_current_date()}</strong><p><br>'''
            new_task = Task.objects.create(
                task_title=f'[Accept Test Campaign Email] {form.instance.audience} - {form.instance.subject}',
                task_type='Email Campaign',
                task_description=task_description,
                task_history_log=history_log,
                assigned_profile=self.request.user.profile,
                email_campaign=email_campaign,
            )

            # Send Email
            email_address = self.request.user.email
            email_subject = form.instance.subject
            email_message = f"""
            {EMAIL_MESSAGE_CAMPAIGN_1}
            *** This is a TEST EMAIL * Please make any changes in the <a href="{EMAIL_CAMPAIGN_DETAIL_URL}{email_campaign.id}/">Email Campaign</a>. ***<br>
            *** Once you are satisfied please update this <a href="{TASK_URL}{task_obj.id}">Task</a> as Revise to send another test email, or Agree to continue the ServiceFlow. ***<p>
            {form.instance.message}
            {EMAIL_MESSAGE_2}
            """
            send_email(email_subject, email_address, email_message)

        message = f'{form.instance.audience} - {form.instance.subject}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The email Campaign, "{message}" has been updated.'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'
        return context


class EmailCampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """EmailCampaign DeleteView."""
    model = EmailCampaign
    context_object_name = 'email_campaign'
    success_url = reverse_lazy('email-campaigns')
    template_name = 'iamown/email_campaign_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
