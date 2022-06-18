from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


# ############ Event Settings form validation logic ############
def profile_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if not cleaned_data.get('phone') and cleaned_data.get('notification_preference') == 'Text/SMS':
        form.add_error(
            'phone',
            'A phone number must be entered in order to be able to receive text messages on your phone.'
        )
    return


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error(
                'email',
                'That email address is already associated with a Whurthy account. Please use another email address.',
            )
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()

        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error(
                'email',
                'That email address is already associated with an account. Please use another email address.',
            )
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'pronoun',
            'spiritual_name',
            'bio',
            'given_first_name',
            'given_last_name',
            'address_1',
            'address_2',
            'city',
            'state_province_county',
            'postal_zip_code',
            'country',
            'phone',
            'notification_preference',
        ]

    def clean(self):
        profile_form_validation(self, ProfileUpdateForm)

        return self.cleaned_data
