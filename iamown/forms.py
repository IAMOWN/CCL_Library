from django import forms
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    Task,
    ServiceGroup,
)

from users.models import (
    Profile,
)


# ############ Task form validation logic ############
def task_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('task_title') is None:
        form.add_error(
            'task_title',
            'A title for the task must be entered.'
        )
        
    print(f"cleaned_data.get('task_type'): {cleaned_data.get('task_type')}")

    if cleaned_data.get('task_status') == 'Completed' \
            and cleaned_data.get('book_text_impacted') == '---' \
            and cleaned_data.get('task_type') == 'Library Observation':
        form.add_error(
            'book_text_impacted',
            '''If uncertain, it is recommended that you select "Yes". Completing the task with "Yes" selected for book 
            text impacted will assign a task to the Book Editing Circle.'''
        )

    return


# ############ Service Group form validation logic ############
def service_group_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('service_group') is None:
        form.add_error(
            'service_group',
            'A name for the Service Group must be entered.'
        )
    return


# ####################### Create Task Form #######################
class CreateTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_profile'].queryset = Profile.objects.filter(user__is_staff=True)

        # self.fields['assigned_dear_soul'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = Task
        fields = [
            'task_title',
            'task_description',
            'actions_taken',
            'assigned_profile',
            'task_status',
            'task_priority',
            'due_date',
            'task_type',
            'book_text_impacted',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        task_form_validation(self, CreateTaskForm)
        return self.cleaned_data


# ####################### Update Task Form #######################
class UpdateTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_profile'].queryset = Profile.objects.filter(user__is_staff=True)

    class Meta:
        model = Task
        fields = [
            'task_title',
            'task_description',
            'actions_taken',
            'assigned_profile',
            'task_status',
            'task_priority',
            'due_date',
            'task_type',
            'book_text_impacted',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        task_form_validation(self, UpdateTaskForm)
        return self.cleaned_data


# ####################### Create Service Group Form #######################
class CreateServiceGroupForm(forms.ModelForm):

    class Meta:
        model = ServiceGroup
        fields = [
            'service_group',
            'purpose',
            'qualified_intentions',
            'service_group_type',
            'service_group_status',
            'dear_souls_in_service_group',
        ]

    def clean(self):
        service_group_form_validation(self, CreateServiceGroupForm)
        return self.cleaned_data


# ####################### Update Service Group Form #######################
class UpdateServiceGroupForm(forms.ModelForm):

    class Meta:
        model = ServiceGroup
        fields = [
            'service_group',
            'purpose',
            'qualified_intentions',
            'service_group_type',
            'service_group_status',
            'dear_souls_in_service_group',
        ]

    def clean(self):
        service_group_form_validation(self, UpdateServiceGroupForm)
        return self.cleaned_data
