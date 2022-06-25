from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Task,
)
from .forms import (
    CreateTaskForm,
    UpdateTaskForm,
)


# ####################### TASK VIEWS #######################
class TaskList(LoginRequiredMixin, ListView):
    """Task ListView for user's tasks."""
    model = Task
    template_name = 'iamown/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['tasks_count'] = Task.objects.all().exclude(task_status='Completed').count()
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
        context['current_user'] = self.request.user

        context['tasks'] = Task.objects.filter(assigned_dear_soul=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()

        return context


# ####################### Task - Create View #######################
class TaskCreate(LoginRequiredMixin, CreateView):
    """Task CreateView for user's tasks."""
    model = Task
    form_class = CreateTaskForm

    template_name = 'iamown/task_form.html'

    def form_valid(self, form):
        form.instance.assigned_dear_soul = self.request.user
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
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()

        return context


# ####################### Task - Update View #######################
class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task UpdateView for user's tasks."""
    model = Task
    form_class = UpdateTaskForm

    template_name = 'iamown/task_form.html'

    # success_url = reverse_lazy('tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assigned_dear_soul or self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['page_type'] = 'Update'
        context['tasks'] = Task.objects.filter(assigned_dear_soul=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()

        return context


# ####################### Task - Completed View #######################
class TaskCompletedList(LoginRequiredMixin, ListView):
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
        task = self.get_object()
        if self.request.user == task.assigned_dear_soul:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDelete, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['tasks'] = Task.objects.filter(assigned_user=self.request.user)
        context['tasks_count'] = context['tasks'].exclude(task_status='Completed').count()

        return context
