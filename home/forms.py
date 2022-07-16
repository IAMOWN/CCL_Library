from django import forms

from iamown.models import (
    Audience,
    MailingList,
)


# ############ Subscription form validation logic ############
def subscription_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('email') is None:
        form.add_error(
            'email',
            'A email address must be entered.'
        )
    else:
        if "@" not in cleaned_data.get('email'):
            form.add_error(
                'email',
                'Your email address must contain an "@" symbol.'
            )
        if "." not in cleaned_data.get('email'):
            form.add_error(
                'email',
                'Your email address must contain at least one period (full-stop).'
            )
    return


# ####################### Subscription Create Form #######################
class CreateSubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audience'].queryset = Audience.objects.all().exclude(scope='Internal')

    class Meta:
        model = MailingList

        fields = [
            'audience',
            'email',
        ]

    def clean(self):
        subscription_form_validation(self, CreateSubscriptionForm)
        return self.cleaned_data


# ####################### Subscription Update Form #######################
class UpdateSubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audience'].queryset = Audience.objects.all().exclude(scope='Internal')

    class Meta:
        model = MailingList

        fields = [
            'audience',
            'email',
        ]

    def clean(self):
        subscription_form_validation(self, UpdateSubscriptionForm)
        return self.cleaned_data
