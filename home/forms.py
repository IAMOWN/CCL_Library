from django import forms

from iamown.models import (
    Audience,
    MailingList,
)


# ############ Subscription form validation logic ############
def subscription_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('email_address') is None:
        form.add_error(
            'email_address',
            'A email address must be entered.'
        )
    return


# ####################### Subscription Create Form #######################
class CreateSubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mailing_list'].queryset = Audience.objects.all().exclude(scope='Internal')

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
        self.fields['mailing_list'].queryset = Audience.objects.all().exclude(scope='Internal')

    class Meta:
        model = MailingList

        fields = [
            'mailing_list',
            'email_address',
        ]

    def clean(self):
        subscription_form_validation(self, UpdateSubscriptionForm)
        return self.cleaned_data
