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
                                <img src="https://ega.s3.us-east-2.amazonaws.com/Soul+Synthesis+Email+Header.png" alt="Soul Synthesis email header banner" width: 600px;"/>
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
                                <img src="https://ega.s3.us-east-2.amazonaws.com/Soul+Synthesis+Email+Footer+-+72.png" alt="Whurthy email header banner" width: 600px;"/>
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


# ####################### Newsletter #######################
def newsletter(request):
    if not request.user.is_authenticated:
        external_audiences = Audience.objects.all().exclude(scope='Internal')
        audience_input = request.GET.get('audience-selection') or ''
        email_address_input = request.GET.get('email-address-entry') or ''
        print(f'audience_input: {audience_input}')
        print(f'email_address_input: {email_address_input}')

        # Get IP
        client_ip, is_routable = get_client_ip(request)
        if client_ip is None:
            ip_result = None
        else:  # There is an IP
            if is_routable:
                ip_result = True  # We got it
            else:
                ip_result = "Private"  # but it's private

        # Check for injection attack
        email_input_safe = True
        for item in INJECTION_LIST:
            print(f'item: {item}')
            if item in email_address_input:
                email_input_safe = False
                print(f'Injection attempt: {item}')
                break

        print(f'email_input_safe: {email_input_safe}')

        # Process initial Opt-In request
        if email_input_safe:
            try:
                email_exists = MailingList.objects.filter(email=email_address_input, audience=audience_input)
                subsciption_outcome_message = f'This email is already subscribed to the {audience_input} mailing list. Love and Blessings.'
            except MailingList.DoesNotExist:
                scope = Audience.objects.get(audience=audience_input).scope
                if audience_input:
                    if ip_result is None:
                        new_subscription = MailingList.objects.create(
                            audience=audience_input,
                            email=email_address_input,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: None</strong> on <strong>{get_current_year()}</strong>''',
                        )
                    elif ip_result:
                        new_subscription = MailingList.objects.create(
                            audience=audience_input,
                            email=email_address_input,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_year()}</strong>''',
                        )

                    elif ip_result == 'Private':
                        new_subscription = MailingList.objects.create(
                            audience=audience_input,
                            email=email_address_input,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: Private</strong> on <strong>{get_current_year()}</strong>''',
                        )

                    subsciption_outcome_message = f'The email, {email_address_input} has been added to the {audience_input} mailing list. Love and Blessings.'
                    print(f'new_subscription: {new_subscription}')
        else:
            subsciption_outcome_message = f'''
            Love and Blessings to you. Your attempt at an injection attack has come to no avail.<p>You are already 
            forgiven, for there is nothing to Forgive in the Heart of God.'''

        print(f'subsciption_outcome_message: {subsciption_outcome_message}')

        # TODO Send confirmation email

        context = {
            'title': 'Newsletter and Mailing List Subscription',
            'external_audiences': external_audiences,
            'subsciption_outcome_message': subsciption_outcome_message,
        }

    else:
        context = {
            'title': 'Newsletter and Mailing List Subscription',
        }

    return render(request, 'home/newsletter.html', context)


# ####################### Create Subscription #######################
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
        # Get IP
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip is None:
            ip_result = None
        else:  # There is an IP
            if is_routable:
                ip_result = True  # We got it
            else:
                ip_result = "Private"  # but it's private

        print(f'client_ip: {client_ip}')

        if self.request.user.is_anonymous:
            print(f'self.request.user: {self.request.user}')
            try:
                email_exists = MailingList.objects.get(email=form.instance.email, audience=form.instance.audience)
                print(f'email_exists: {email_exists}')
                form.add_error(
                    'email',
                    f'The email "{form.instance.email}" is already subscribed to the {form.instance.audience} mailing list. Love and Blessings.',
                )
                return self.form_invalid(form)

            except MailingList.DoesNotExist:
                print('Does not exist')
                if audience_input:
                    if ip_result is None:
                        new_subscription = MailingList.objects.create(
                            audience=form.instance.audience,
                            email=form.instance.email,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: None</strong> on <strong>{get_current_year()}</strong>''',
                        )
                    elif ip_result:
                        new_subscription = MailingList.objects.create(
                            audience=form.instance.audience,
                            email=form.instance.email,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_year()}</strong>''',
                        )
                    elif ip_result == 'Private':
                        new_subscription = MailingList.objects.create(
                            audience=form.instance.audience,
                            email=form.instance.email,
                            subscribed='Unconfirmed',
                            mailing_list_log=f'''>>> <strong>First Opt-In Subscription</strong> from <strong>IP: Private</strong> on <strong>{get_current_year()}</strong>''',
                        )

                    subject = f'Please confirm your subscription to the Cosmic Christ Love Newsletter {form.instance.audience} mailing list'
                    email_message = f'''
                        {EMAIL_MESSAGE_CAMPAIGN_1}
                        Beloved,<p>
                        Please confirm your subscription to the Cosmic Christ Love {form.instance.audience} mailing list by clicking this <a href="{CONFIRM_SUBSCRIPTION_URL}{form.instance.audience}/{form.instance.email}/">link</a>.<p>
                        Love and Blessings,<br>
                        The Elemental Grace Alliance.
                        {EMAIL_MESSAGE_2}
                    '''
                    send_email(subject, form.instance.email, email_message)

                    subsciption_outcome_message = f'Thank you. An email to confirm your email subscription has been sent to {form.instance.email}. Love and Blessings.'

                messages.add_message(
                    messages.SUCCESS,
                    f'{subsciption_outcome_message}'
                )

                # TODO Variable to hide the form and return to subscribe with the message
                return super().form_valid(form)

        return super().form_valid(form)

def subscription_confirm(request):
    subscription_confirmed = False
    # Get IP
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
        subscription = MailingList.objects.get(audience=audience, email=email)
        if subscription.subscribed == 'Yes':
            subsciption_outcome_message = f'The email "{email}" is already subscribed to the {audience} mailing list. There is nothing more you need do.<p>Love and Blessings,<br>The Elemental Grace Alliance'
            subscription_confirmed = True
        else:
            subscription.subscribed = 'Yes'
            subscription_confirmed = True
            if ip_result is None:
                subscription.mailing_list_log = f'''>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: None</strong> on <strong>{get_current_year()}</strong>'''
            elif ip_result:
                subscription.mailing_list_log = f'''>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: {client_ip}</strong> on <strong>{get_current_year()}</strong>''',
            elif ip_result == 'Private':
                subscription.mailing_list_log = f'''>>> <strong>Second Opt-In Subscription</strong> from <strong>IP: Private</strong> on <strong>{get_current_year()}</strong>''',
            subscription.save(update_fields=[
                'subscribed',
                'mailing_list_log',
            ])
    except MailingList.DoesNotExist:
        subsciption_outcome_message = f'''The email "{email} is not currently subscribed to the {audience} mailing list. If you wish to subscribe this email then please do so <a href="{SUBSCRIPTION_URL}" class="">here</a>.<p>Love and Blessings,<br>The Elemental Grace Alliance'''

    if subscription_confirmed:
        context = {
            'subsciption_outcome_message': subsciption_outcome_message,
            'title': f'Your Subscription Is Confirmed',
        }
    else:
        context = {
            'subsciption_outcome_message': subsciption_outcome_message,
            'title': f'Your Subscription',
        }

    return render(request, 'home/subscription_confirm.html', context)
