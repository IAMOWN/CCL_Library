from django import forms

from iamown.models import (
    Audience,
    MailingList,
)


# ############ Subscription form validation logic ############
def subscription_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    email = cleaned_data.get('email')
    print(f'email.type: {email.type()}')
    if email is None:
        form.add_error(
            'email',
            'A email address must be entered.'
        )
    elif "@" not in email:
        form.add_error(
            'email',
            'Your email address must contain an "@" symbol.'
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
