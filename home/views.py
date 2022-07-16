from datetime import datetime, timezone

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from ipware import get_client_ip

from iamown.models import (
    Audience,
    MailingList,
)

from home.forms import (
    CreateSubscriptionForm,
    UpdateSubscriptionForm,
)

# ####################### CONSTANTS #######################
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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Header.png" alt="Soul Synthesis email header banner" width: 600px;"/>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td class="ms-rteTableEvenCol-0" align="left">
                              <div>
                                <p>
                                <span style="color: #000000; background-color: transparent; font-family: arial;">
'''
EMAIL_MESSAGE_CAMPAIGN_1 = '''
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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Header%20-%20Campaign.png" alt="Soul Synthesis email header banner" width: 600px;"/>
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
                                <a href="https://cosmicchrist.love/"><img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/CCL%20Email%20Footer.png" alt="Whurthy email header banner" width: 600px;" style="border: 0;" /></a>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </body>
                    </html>
'''
FROM_EMAIL = 'info@lanesflow.io'
CONTACT_EMAIL = 'egaadministration@protonmail.com'
INJECTION_LIST = [
    "<script>",
    "</script>",
    "<html>",
    "</html>",
    "<body>",
    "</body>",
    "<input>",
    "SELECT",
    "NULL",
    "UNION",
    "<#>",
    "</>",
    "<-->",
]
SUBSCRIPTION_URL = 'https://cosmicchrist.love/subscribe/'
CONFIRM_SUBSCRIPTION_URL = 'https://cosmicchrist.love/confirm_subscription/'

# FUNCTIONS
def send_email(subject, to_email, message):
    send_mail(
        subject,
        message,
        FROM_EMAIL,
        [to_email],
        fail_silently=False,
        html_message=message,
    )


# ####################### FUNCTIONS #######################
def get_current_year():
    return datetime.now(tz=timezone.utc).year

def get_current_date():
    return datetime.now().date()


# ####################### BASIC VIEWS #######################
def home(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Cosmic Christ Love',
            'year': get_current_year(),
        }
    else:
        context = {
            'title': 'Cosmic Christ Love',
            'year': get_current_year(),
        }

    return render(request, 'home.html', context)


# ####################### Contact #######################
def contact(request):
    if request.method == 'POST':
        contact_name = request.POST['message-name']
        contact_email = request.POST['message-email']
        message = request.POST['message']

        email_subject = f'CCL Library Contact: {contact_name}'
        email_message = f"""
        {EMAIL_MESSAGE_1}
        <p><strong>Contact request from:</strong> {contact_name}</p>
        <p><strong>Email:</strong> {contact_email}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>        
        {EMAIL_MESSAGE_2}
        """
        send_email(email_subject, CONTACT_EMAIL, email_message)

        context = {
            'name': contact_name,
            'valid': True,
            'confirm_message_1': "Thanks for contacting us, ",
            'confirm_message_2': "Your message has been sent and we will respond as soon as we can.",
            'confirm_message_3': "Love and Blessings, The Elemental Grace Alliance",
        }

        return render(request, 'home/contact.html', context)

    else:
        return render(request, 'home/contact.html')


# ####################### Search Training #######################
def training(request):
    context = {
        'title': 'How To Make The Most Of Search',
        'year': get_current_year(),
    }

    return render(request, 'training.html', context)


# ####################### Librarian Training #######################
@login_required
def librian_training(request):
    context = {
        'title': 'Librarian Training Videos',
        'year': get_current_year(),
    }

    return render(request, 'librarian_training.html', context)


# ####################### Release Notes #######################
@login_required
def release_notes(request):
    context = {
        'title': 'Release Notes',
        'year': get_current_year(),
    }

    return render(request, 'release_notes.html', context)


# ####################### Create Subscription (First Opt-In) #######################
class SubscriptionCreate(CreateView):
    model = MailingList
    form_class = CreateSubscriptionForm
    template_name = 'home/newsletter_subscription_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'
        return context

    def form_valid(self, form):
        # Get IP Address
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip is None:
            ip_result = None
        else:  # There is an IP
            if is_routable:
                ip_result = True  # We got it
            else:
                ip_result = "Private"  # but it's private

        if self.request.user.is_anonymous:
            # Check for user account with this email address
            try:
                user = User.objects.get(email=form.instance.email)
                try:
                    # Check for user account already subscribed to Audience
                    user_subscribed = MailingList.objects.get(audience=form.instance.audience, user__username=user)
                    form.add_error(
                        'email',
                        f'This email address is associated with a Cosmic Christ Love account already subscribed to the {form.instance.audience} mailing list. Please enter another email address.'
                    )
                    return self.form_invalid(form)

                # Create user subscription entry for mailing list
                except MailingList.DoesNotExist:
                    form.instance.email = ''
                    form.instance.user = user
                    form.instance.subscribed = 'Yes'
                    if ip_result is None:
                        form.instance.mailing_list_log = f'''>>> <strong>User Subscription for email</strong> from <strong>IP: None</strong> on <strong>{get_current_date()}</strong>'''
                    elif ip_result:
                        form.instance.mailing_list_log = f'''>>> <strong>User Subscription for email</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_date()}</strong>'''
                    elif ip_result == 'Private':
                        form.instance.mailing_list_log = f'''>>> <strong>User Subscription for email</strong> from <strong>IP: Private</strong> on <strong>{get_current_date()}</strong>'''

                    # Create flash message for successful subscription
                    subsciption_outcome_message = f'Bless You. This user account has been added to the {form.instance.audience} mailing list. Nothing further need be done. Love and Blessings.'
                    messages.add_message(
                        self.request,
                        messages.SUCCESS,
                        f'{subsciption_outcome_message}'
                    )
                    return super().form_valid(form)

            except User.DoesNotExist:
                # Check if email is already subscribed to this mailing list
                try:
                    email_exists = MailingList.objects.get(email=form.instance.email, audience=form.instance.audience)
                    form.add_error(
                        'email',
                        f'The email "{form.instance.email}" is already subscribed to the {form.instance.audience} mailing list. Love and Blessings.',
                    )
                    return self.form_invalid(form)

                # If the email is not already subscribed update the new subscription log with entry and change subscription status to Unconfirmed
                except MailingList.DoesNotExist:
                    form.instance.subscribed = 'Unconfirmed'
                    if ip_result is None:
                        form.instance.mailing_list_log = f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: None</strong> on <strong>{get_current_date()}</strong>'''
                    elif ip_result:
                        form.instance.mailing_list_log = f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_date()}</strong>'''
                    elif ip_result == 'Private':
                        form.instance.mailing_list_log = f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: Private</strong> on <strong>{get_current_date()}</strong>'''

                    # Send subscription confirmation email
                    subject = f'Please confirm your subscription to the Cosmic Christ Love Newsletter {form.instance.audience} mailing list'
                    email_message = f'''
                        {EMAIL_MESSAGE_CAMPAIGN_1}
                        Beloved,<p>
                        Please <strong>confirm your subscription</strong> by clicking this <strong><a href="{CONFIRM_SUBSCRIPTION_URL}{form.instance.audience}/{form.instance.email}/">link</a></strong>.<p>
                        Love and Blessings,<br>
                        The Elemental Grace Alliance.
                        {EMAIL_MESSAGE_2}
                    '''
                    send_email(subject, form.instance.email, email_message)

                    # Create flash message
                    subsciption_outcome_message = f'Bless You. An email to confirm your email subscription has been sent to {form.instance.email}. Love and Blessings.'
                    messages.add_message(
                        self.request,
                        messages.SUCCESS,
                        f'{subsciption_outcome_message}'
                    )
                    return super().form_valid(form)
                    # TODO Variable to hide the form and return to subscribe with the message

        else:  # TODO Process user trying to subscribe
            return super().form_valid(form)


# ####################### Confirm Subscription (Second Opt-In) #######################
def subscription_confirm(request, audience, email):
    subscription_confirmed = False
    # Get IP Address
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        ip_result = None
    else:  # There is an IP
        if is_routable:
            ip_result = True  # We got it
        else:
            ip_result = "Private"  # but it's private

    # Process Second Opt-In request
    try:
        subscription = MailingList.objects.get(audience__audience=audience, email=email)
        # Check that the user has not already confirmed
        if subscription.subscribed == 'Yes':
            subsciption_outcome_message = f'The email "{email}" is already subscribed to the {audience} mailing list. There is nothing more you need do.<p>Love and Blessings,<br>The Elemental Grace Alliance'
            subscription_confirmed = True
        # Add the Second Opt-in event to the mailing_list_log and update the subscription status
        else:
            subscription.subscribed = 'Yes'
            subscription_confirmed = True
            if ip_result is None:
                subscription.mailing_list_log = subscription.mailing_list_log + f'''<br>>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: None</strong> on <strong>{get_current_date()}</strong>'''
            elif ip_result:
                subscription.mailing_list_log = subscription.mailing_list_log + f'''<br>>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_date()}</strong>'''
            elif ip_result == 'Private':
                subscription.mailing_list_log = subscription.mailing_list_log + f'''<br>>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: Private</strong> on <strong>{get_current_date()}</strong>'''
            subscription.save(update_fields=[
                'subscribed',
                'mailing_list_log',
            ])
            subsciption_outcome_message = f'''Thank you for confirming your subscription to the Cosmic Christ Love {audience} mailing list.<p>Love and Blessings,<br>The Elemental Grace Alliance'''

    # The First Opt-In stap has not been completed. Direct the user to the subscription page.
    except MailingList.DoesNotExist:
        subsciption_outcome_message = f'''The email "{email} is not currently subscribed to the {audience} mailing list. If you wish to subscribe this email then please do so <a href="{SUBSCRIPTION_URL}" class="">here</a>.<p>Love and Blessings,<br>The Elemental Grace Alliance'''

    context = {
        'subsciption_outcome_message': subsciption_outcome_message,
        'title': f'Your Subscription Is Confirmed',
    }
    return render(request, 'home/subscription_confirm.html', context)
