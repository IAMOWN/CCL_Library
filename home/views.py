from datetime import datetime, timezone

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from iamown.models import (
    MailingList,
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


# DATE LOGIC
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
        external_audiences = MailingList.objects.exclude(audience__scope='Internal')
        audiences = request.GET.get('audience-selection') or ''
        email_address = request.GET.get('email-address-entry') or ''

        context = {
            'external_audiences': external_audiences,
            'title': 'Newsletter and Mailing List Subscription',
        }

    else:
        context = {
            'title': 'Newsletter and Mailing List Subscription',
        }

    return render(request, 'home/newsletter.html', context)
