from django.shortcuts import render
from django.conf import settings
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

from datetime import datetime

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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/Soul%20Synthesis%20Email%20Header.png" alt="Soul Synthesis email header banner" width: 600px;"/>
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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/Soul%20Synthesis%20Email%20Footer%20-%2072.png" alt="Whurthy email header banner" width: 600px;"/>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </body>
                    </html>
'''
LIBRARY_TASK_URL = 'https://cosmicchrist.love/tasks/library/'

LEE_TASK_NAME_BOOK_FILE_REVIEW = 'Book File Review'
BOOK_EDITOR_GROUP_NAME = 'Book Editors'

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
        context = super(LEEDetailView, self).get_context_data(**kwargs)

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
        return super(LEECreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LEECreateView, self).get_context_data(**kwargs)
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
        return super(LEEUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LEEUpdateView, self).get_context_data(**kwargs)
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
        context = super(LEEDeleteView, self).get_context_data(**kwargs)

        return context


# ####################### TASK VIEWS #######################
class TaskList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task ListView for user's tasks."""
    model = Task
    template_name = 'iamown/tasks.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter().exclude(task_status='Completed').order_by(
            'task_status',
            'task_priority',
            'due_date',
        )
        context['tasks'] = tasks
        context['tasks_count'] = tasks.count()
        context['completed_tasks_count'] = Task.objects.filter(task_status='Completed').count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(task_title__icontains=search_input)  # Can also use __startswith
        context['search_input'] = search_input

        context['search_off'] = True
        assignee_search_input = self.request.GET.get('assignee-search-area') or ''
        task_search_input = self.request.GET.get('task-search-area') or ''
        status_search_input = self.request.GET.get('status-search-area') or ''
        priority_search_input = self.request.GET.get('priority-search-area') or ''
        context['search_count'] = 0
        if assignee_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(assigned_user__username=assignee_search_input)
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Assignee'
            context['search_entered'] = assignee_search_input
        # elif task_search_input:
        #     context['search_off'] = False
        #     context['tasks'] = context['tasks'].filter(task_title__icontains=task_search_input)
        #     context['search_count'] = context['tasks'].count()
        #     context['search_type'] = 'Task'
        #     context['search_entered'] = task_search_input
        elif status_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(task_status__icontains=status_search_input)
            context['search_count'] = context['tasks'].count()
            context['search_type'] = 'Status'
            context['search_entered'] = status_search_input
        elif priority_search_input:
            context['search_off'] = False
            context['tasks'] = context['tasks'].filter(task_priority__icontains=priority_search_input)
            context['search_count'] = context['tasks'].exclude(task_status='Completed').count()
            context['search_type'] = 'Priority'
            context['search_entered'] = priority_search_input

        return context


# ####################### Task - Detail View #######################
class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task DetailView for user's tasks."""
    model = Task
    template_name = 'iamown/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)

        return context


# ####################### Task - Create View #######################
class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Task CreateView for user's tasks."""
    model = Task
    form_class = CreateLibraryTaskForm

    template_name = 'iamown/task_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been added'
        )
        return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['page_type'] = 'Create'

        return context


# ####################### Task - Update View #######################
class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task UpdateView for user's tasks."""
    model = Task
    form_class = UpdateLibraryTaskForm

    template_name = 'iamown/task_form.html'

    def test_func(self):
        # task = self.get_object()
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)

        context['current_user'] = self.request.user
        context['page_type'] = 'Update'
        # context['tasks'] = Task.objects.filter(task_status='Completed')
        # context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()

        return context

    def form_valid(self, form):
        library_task = form.save(commit=False)
        task_updater = Profile.objects.get(user__username=self.request.user).spiritual_name
        if library_task.task_status == 'Completed':
            library_task.date_completed = get_current_date()
            library_task.task_history_log = library_task.task_history_log + f'''>>> Task type: <strong>{form.instance.task_type}</strong> manually updated by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br>
            Date completed: <strong>{library_task.date_completed}</strong> >>> Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p>
            '''
            library_task.save(update_fields=['task_history_log','date_completed',])
        else:
            library_task.task_history_log = library_task.task_history_log + f'''>>> Task type: <strong>{form.instance.task_type}</strong> manually updated by <strong>{task_updater}</strong> on <strong>{get_current_date()}</strong>.<br>
            Status: <strong>{form.instance.task_status}</strong> >>> Priority: {form.instance.task_priority} >>> Due date: {form.instance.due_date} >>> Assigned Dear Soul: {form.instance.assigned_profile} >>> Assigned Group: {form.instance.assigned_service_group}<p>
            '''
            library_task.save(update_fields=['task_history_log',])
        message = form.instance.task_title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Task "{message}" has been updated'
        )
        return super(TaskUpdate, self).form_valid(form)


# ####################### Task - Completed View #######################
class TaskCompletedList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task ListView for user's completed tasks."""
    model = Task
    template_name = 'iamown/tasks_completed.html'
    context_object_name = 'tasks'

    def test_func(self):
        if self.request.user.is_staff:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['tasks'] = Task.objects.all().filter(task_status='Completed')
        context['completed_tasks_count'] = Task.objects.filter(task_status='Completed').count()
        context['tasks_count'] = Task.objects.all().exclude(task_status='Completed').count()

        return context


# ####################### Task - Delete View #######################
class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Task DeleteView for user's tasks."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'iamown/task_confirm_delete.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDelete, self).get_context_data(**kwargs)

        return context


# ####################### Library Tasks - List View #######################
class TaskLibraryList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task ListView for Library Observation tasks."""
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
            context['tasks'] = context['tasks'].filter(task_title__icontains=search_input)  # Can also use __startswith
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
            search_result = Task.objects.filter(assigned_profile__spiritual_name=assignee_search_input).order_by(
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
            search_result = Task.objects.filter(task_status__icontains=status_search_input).order_by(
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
            search_result = Task.objects.filter(task_priority__icontains=priority_search_input).order_by(
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


# ####################### Task Libary - Detail View #######################
class TaskLibraryDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task DetailView for Library Observation tasks."""
    model = Task
    template_name = 'iamown/task_detail_library.html'
    context_object_name = 'task'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskLibraryDetail, self).get_context_data(**kwargs)

        return context


# ####################### Tasks Library - Completed View #######################
class TaskLibraryCompletedList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Task TaskLibraryCompletedList for completed Library Observation tasks."""
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


# ####################### Task Library - Create View #######################
class TaskLibraryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Task CreateView for user's tasks."""
    model = Task
    form_class = CreateLibraryTaskForm

    template_name = 'iamown/task_form.html'

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
        return super(TaskLibraryCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskLibraryCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Task Library - Update View #######################
class TaskLibraryUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task UpdateView for Library tasks."""
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
        context = super(TaskLibraryUpdate, self).get_context_data(**kwargs)
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

                history_log = f'''>>> <strong>{LEE_TASK_NAME_BOOK_FILE_REVIEW}</strong> task created from completed Library Observation task: {related_task.task_title}<p><br>'''
                task_description = LEE.objects.get(task_name=LEE_TASK_NAME_BOOK_FILE_REVIEW).process_description
                if library_task.book_urls_for_record:
                    task_description = task_description + f'''<strong>Book urls:</strong><br>
                    {library_task.book_urls_for_record}
                '''
                else:
                    task_description = task_description + '<strong>There are no book urls listed for this record.</strong>'

                created_task = Task.objects.create(
                    task_title=f'{LEE_TASK_NAME_BOOK_FILE_REVIEW} Check Book Files related to Library Observation',
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
                        email_subject = f'[CCL] A corrected Library observation has been marked as having an impact on book text.'
                        email_message = f"""
                        {EMAIL_MESSAGE_1}
                        Beloved {editor.profile.spiritual_name},<p>
                        A Library Observation has just been completed, and has been marked as having an impact on book text 
                        related to the Library record.<p> 
                        Please review the <a href='{LIBRARY_TASK_URL}'>Library Tasks</a> at your earliest convenience.<p>
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
            f'The Task "{message}" has been updated'
        )
        return super(TaskLibraryUpdate, self).form_valid(form)


# ####################### Task Library - Delete View #######################
class TaskLibraryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Task DeleteView for Library Observation tasks."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks-library')
    template_name = 'iamown/task_confirm_delete_library.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskLibraryDelete, self).get_context_data(**kwargs)
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


# ####################### Service Group - Detail View #######################
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


# ####################### Service Group - Create View #######################
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
        return super(ServiceGroupCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Service Group - Update View #######################
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
        return super(ServiceGroupUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


# ####################### Service Group - Delete View #######################
class ServiceGroupDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceGroup
    template_name = 'iamown/service_group_confirm_delete.html'
    success_url = reverse_lazy('service-groups')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceGroupDelete, self).get_context_data(**kwargs)

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
        context = super(PEePDetailView, self).get_context_data(**kwargs)

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
        return super(PEePCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PEePCreateView, self).get_context_data(**kwargs)
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
        return super(PEePUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PEePUpdateView, self).get_context_data(**kwargs)
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
        context = super(PEePDeleteView, self).get_context_data(**kwargs)

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
        context = super(AudienceDetailView, self).get_context_data(**kwargs)
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
        message = form.instance.audience
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The audience "{message}" has been added.'
        )
        return super(AudienceCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AudienceCreateView, self).get_context_data(**kwargs)
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
        return super(AudienceUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AudienceUpdateView, self).get_context_data(**kwargs)
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
        context = super(AudienceDeleteView, self).get_context_data(**kwargs)
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
        return context


class MailingListDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """MailingList DetailView."""
    model = MailingList
    template_name = 'iamown/mailing_list_detail.html'
    context_object_name = 'mailing_list_entry'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(MailingListDetailView, self).get_context_data(**kwargs)
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

    def form_valid(self, form):
        if form.instance.user:
            message = f'{form.instance.audience}: {form.instance.user}'
        else:
            message = f'{form.instance.audience}: {form.instance.email}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The mailing list entry, "{message}" has been added.'
        )
        return super(MailingListCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(MailingListCreateView, self).get_context_data(**kwargs)
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
            message = f'{form.instance.audience}: {form.instance.user}'
        else:
            message = f'{form.instance.audience}: {form.instance.email}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The mailing list entry, "{message}" has been updated.'
        )
        return super(MailingListUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(MailingListUpdateView, self).get_context_data(**kwargs)
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
        context = super(MailingListDeleteView, self).get_context_data(**kwargs)
        return context


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
        context = super(EmailCampaignDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Email campaign: {self.audience} - {self.subject}'
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
        message = f'{form.instance.audience} - {form.instance.subject}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The email campaign, "{message}" has been created.'
        )
        return super(MailingListCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(EmailCampaignCreateView, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        return context


class EmailCampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """EmailCampaign UpdateView."""
    model = EmailCampaign
    form_class = UpdateEmailCampaignForm

    template_name = 'iamown/email_campaign_form.html'
    success_url = reverse_lazy('email_campaigns')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        message = f'{form.instance.audience} - {form.instance.subject}'
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The email campaign, "{message}" has been updated.'
        )
        return super(EmailCampaignUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(EmailCampaignUpdateView, self).get_context_data(**kwargs)
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
        context = super(EmailCampaignDeleteView, self).get_context_data(**kwargs)
        return context
