from django import forms
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    Task,
    ServiceGroup,
    LEE,
    PEeP,
    Audience,
    MailingList,
    EmailCampaign,
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
    if cleaned_data.get('decision') == 'Revise' and form.instance.task_type == 'Email Campaign':
        form.add_error(
            'decision_comments',
            '''If your decision is to Revise then you are asked to note why.'''
        )
    elif cleaned_data.get('decision') == 'Decline' and form.instance.task_type == 'Email Campaign':
        form.add_error(
            'decision_comments',
            '''If your decision is to Decline then you are asked to note why.'''
        )
    return


# ############ Libary Task form validation logic ############
def library_task_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('task_title') is None:
        form.add_error(
            'task_title',
            'A title for the task must be entered.'
        )
    if cleaned_data.get('task_status') == 'Completed' and cleaned_data.get('book_text_impacted') == '---' and form.instance.task_type == 'Library Observation':
        form.add_error(
            'book_text_impacted',
            '''If you are uncertain then select "Yes". Completing the task with "Yes" selected for book 
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


# ############ PEeP validation logic ############
def PEeP_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('functional_activity') is None:
        form.add_error(
            'functional_activity',
            'A Functional Activity must be entered.'
        )
    return


# ############ LEE validation logic ############
def LEE_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('task_name') is None:
        form.add_error(
            'task_name',
            'A Task Name must be entered.'
        )
    return


# ############ Audience form validation logic ############
def audience_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('audience') == '':
        form.add_error(
            'audience',
            'An audience must be entered.'
        )
    return


# ############ Mailing List form validation logic ############
def mailing_list_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('audience') == '':
        form.add_error(
            'audience',
            'An audience must be selected.'
        )
    if cleaned_data.get('email') is None and cleaned_data.get('user') is None:
        form.add_error(
            'user',
            'Either an email must be entered or existing user account must be selected.'
        )
    return


# ############ Email Campaign form validation logic ############
def email_campaign_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('audience') is None:
        form.add_error(
            'audience',
            'An audience must be selected.'
        )
    if cleaned_data.get('subject') is None:
        form.add_error(
            'subject',
            'An subject must be entered.'
        )
    if cleaned_data.get('message') is None:
        form.add_error(
            'message',
            'An message must be entered.'
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
            'decision',
            'decision_comments',
            'task_type',
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
        self.fields['task_description'].label = False
        self.fields['actions_taken'].label = False
        self.fields['library_task_description'].label = False
        self.fields['library_task_actions_taken'].label = False

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
            'decision',
            'decision_comments',
            'task_type',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        task_form_validation(self, UpdateTaskForm)
        return self.cleaned_data


# ####################### Create Library Task Form #######################
class CreateLibraryTaskForm(forms.ModelForm):

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
            'book_text_impacted',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        library_task_form_validation(self, CreateLibraryTaskForm)
        return self.cleaned_data


# ####################### Update Library Task Form #######################
class UpdateLibraryTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_profile'].queryset = Profile.objects.filter(user__is_staff=True)
        self.fields['task_description'].label = False
        self.fields['actions_taken'].label = False
        self.fields['library_task_description'].label = False
        self.fields['library_task_actions_taken'].label = False

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
            'book_text_impacted',
            'library_task_description',
            'library_task_actions_taken',
        ]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        library_task_form_validation(self, UpdateLibraryTaskForm)
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


# ####################### LEE Create Form #######################
class CreateLEEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsible_for_entry'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = LEE
        fields = [
            'task_name',
            'process_description',
            'responsible_for_entry',
            'process_code',
            'process_outcome',
            'application',
            'relevant_django_file',
        ]

    def clean(self):
        LEE_form_validation(self, CreateLEEForm)
        return self.cleaned_data


# ####################### LEE Update Form #######################
class UpdateLEEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsible_for_entry'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = LEE
        fields = [
            'task_name',
            'process_description',
            'responsible_for_entry',
            'process_code',
            'process_outcome',
            'application',
            'relevant_django_file',
        ]

    def clean(self):
        LEE_form_validation(self, UpdateLEEForm)
        return self.cleaned_data


# ####################### PEeP Create Form #######################
class CreatePEePForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dear_soul_responsible'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = PEeP

        fields = [
            'functional_activity',
            'detailed_description',
            'dear_soul_responsible',
            'service_group',
            'process_code',
        ]

    def clean(self):
        PEeP_form_validation(self, CreatePEePForm)
        return self.cleaned_data


# ####################### PEeP Update Form #######################
class UpdatePEePForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dear_soul_responsible'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = PEeP

        fields = [
            'functional_activity',
            'detailed_description',
            'dear_soul_responsible',
            'service_group',
            'process_code',
        ]

    def clean(self):
        PEeP_form_validation(self, UpdatePEePForm)
        return self.cleaned_data


# ####################### Audience Create Form #######################
class CreateAudienceForm(forms.ModelForm):

    class Meta:
        model = Audience

        fields = [
            'audience',
            'scope',
            'audience_notes',
        ]

    def clean(self):
        audience_form_validation(self, CreateAudienceForm)
        return self.cleaned_data


# ####################### Audience Update Form #######################
class UpdateAudienceForm(forms.ModelForm):

    class Meta:
        model = Audience

        fields = [
            'audience',
            'scope',
            'audience_notes',
        ]

    def clean(self):
        audience_form_validation(self, UpdateAudienceForm)
        return self.cleaned_data


# ####################### Mailing List Create Form #######################
class CreateMailingListForm(forms.ModelForm):

    class Meta:
        model = MailingList

        fields = [
            'audience',
            'email',
            'user',
            'subscribed',
        ]

    def clean(self):
        mailing_list_form_validation(self, CreateMailingListForm)
        return self.cleaned_data


# ####################### Mailing List Update Form #######################
class UpdateMailingListForm(forms.ModelForm):

    class Meta:
        model = MailingList

        fields = [
            'audience',
            'email',
            'user',
            'subscribed',
        ]

    def clean(self):
        mailing_list_form_validation(self, UpdateMailingListForm)
        return self.cleaned_data


# ####################### Email Campaign Create Form #######################
class CreateEmailCampaignForm(forms.ModelForm):

    class Meta:
        model = EmailCampaign

        fields = [
            'audience',
            'subject',
            'message',
            'ready_to_send',
        ]

    def clean(self):
        email_campaign_form_validation(self, CreateEmailCampaignForm)
        return self.cleaned_data


# ####################### Email Campaign Update Form #######################
class UpdateEmailCampaignForm(forms.ModelForm):

    class Meta:
        model = EmailCampaign

        fields = [
            'audience',
            'subject',
            'message',
            'ready_to_send',
        ]

    def clean(self):
        email_campaign_form_validation(self, UpdateEmailCampaignForm)
        return self.cleaned_data
