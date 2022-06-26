from django import forms
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    Task,
)


# ############ Task form validation logic ############
def task_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('task_title') is None:
        form.add_error(
            'task_title',
            'A title for the task must be entered.'
        )
    return


# ####################### Create Task Form #######################
class CreateTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_dear_soul'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = Task
        fields = [
            'task_title',
            'assigned_dear_soul',
            'task_description',
            # 'assigned_team',
            'task_status',
            'task_priority',
            'due_date',
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
        self.fields['assigned_dear_soul'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = Task
        fields = [
            'task_title',
            'assigned_dear_soul',
            'task_description',
            # 'assigned_team',
            'task_status',
            'task_priority',
            'due_date',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    # def clean(self):
    #     task_form_validation(self, UpdateTaskForm)
    #     return self.cleaned_data
