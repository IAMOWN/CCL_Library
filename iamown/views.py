from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
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
)
from .forms import (
    CreateTaskForm,
    UpdateTaskForm,
    CreateServiceGroupForm,
    UpdateServiceGroupForm,
)

from users.models import (
    Profile,
)

# FUNCTIONS
def get_current_year():
    return datetime.now().year

def get_current_date():
    return datetime.now().date()


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
    form_class = CreateTaskForm

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
    form_class = UpdateTaskForm

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
            task_type='Library Observation',
        ).exclude(task_status='Completed').order_by(
            'task_status',
            'task_priority',
            'due_date',
        )
        # TODO Check tasks count on tasks library template
        context['tasks'] = tasks
        context['tasks_count'] = tasks.count()
        context['completed_tasks_count'] = Task.objects.filter(
            task_type='Library Observation',
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

        context['title'] = 'Library Observation Tasks'

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
            task_type='Library Observation',
            task_status='Completed',
        ).order_by(
            '-due_date',
        )
        context['tasks'] = tasks
        context['completed_tasks_count'] = tasks.count()
        context['tasks_count'] = Task.objects.filter(
            task_type='Library Observation',
        ).exclude(task_status='Completed').count()
        context['title'] = 'Completed Library Observation Tasks'

        return context


# ####################### Task Library - Create View #######################
class TaskLibraryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Task CreateView for user's tasks."""
    model = Task
    form_class = CreateTaskForm

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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()

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
        context['year'] = get_current_year()

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
        context['year'] = get_current_year()

        return context
