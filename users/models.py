from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from phone_field import PhoneField

from tinymce.models import HTMLField


# ####################### CHOICE CONSTANTS #######################
PRONOUN_CHOICES = [
    ('---', '---'),
    ('She/her', 'She/her'),
    ('He/him', 'He/him'),
    ('They/them', 'They/them'),
    ('Rather not say', 'Rather not say'),
]
COUNTRY_CHOICES = [
    ('---', '---'),
    ('Canada', 'Canada'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
    ('Afghanistan', 'Afghanistan'),
    ('Aland Islands (Finland)', 'Aland Islands (Finland)'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('American Samoa (USA)', 'American Samoa (USA)'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Anguilla (UK)', 'Anguilla (UK)'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Aruba (Netherlands)', 'Aruba (Netherlands)'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bermuda (UK)', 'Bermuda (UK)'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),
    ('British Virgin Islands (UK)', 'British Virgin Islands (UK)'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burma', 'Burma'),
    ('Burundi', 'Burundi'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Cape Verde', 'Cape Verde'),
    ('Caribbean Netherlands (Netherlands)', 'Caribbean Netherlands (Netherlands)'),
    ('Cayman Islands (UK)', 'Cayman Islands (UK)'),
    ('Central African Republic', 'Central African Republic'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Christmas Island (Australia)', 'Christmas Island (Australia)'),
    ('Cocos (Keeling) Islands (Australia)', 'Cocos (Keeling) Islands (Australia)'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Cook Islands (NZ)', 'Cook Islands (NZ)'),
    ('Costa Rica', 'Costa Rica'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Curacao (Netherlands)', 'Curacao (Netherlands)'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Ethiopia', 'Ethiopia'),
    ('Falkland Islands (UK)', 'Falkland Islands (UK)'),
    ('Faroe Islands (Denmark)', 'Faroe Islands (Denmark)'),
    ('Federated States of Micronesia', 'Federated States of Micronesia'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('French Guiana (France)', 'French Guiana (France)'),
    ('French Polynesia (France)', 'French Polynesia (France)'),
    ('Gabon', 'Gabon'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Gibraltar (UK)', 'Gibraltar (UK)'),
    ('Greece', 'Greece'),
    ('Greenland (Denmark)', 'Greenland (Denmark)'),
    ('Grenada', 'Grenada'),
    ('Guadeloupe (France)', 'Guadeloupe (France)'),
    ('Guam (USA)', 'Guam (USA)'),
    ('Guatemala', 'Guatemala'),
    ('Guernsey (UK)', 'Guernsey (UK)'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Honduras', 'Honduras'),
    ('Hong Kong (China)', 'Hong Kong (China)'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran', 'Iran'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Isle of Man (UK)', 'Isle of Man (UK)'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Ivory Coast', 'Ivory Coast'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jersey (UK)', 'Jersey (UK)'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Kosovo', 'Kosovo'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Laos', 'Laos'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libya', 'Libya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Macau (China)', 'Macau (China)'),
    ('Macedonia', 'Macedonia'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Martinique (France)', 'Martinique (France)'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mayotte (France)', 'Mayotte (France)'),
    ('Mexico', 'Mexico'),
    ('Moldov', 'Moldov'),
    ('Monaco', 'Monaco'),
    ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Montserrat (UK)', 'Montserrat (UK)'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('New Caledonia (France)', 'New Caledonia (France)'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('Niue (NZ)', 'Niue (NZ)'),
    ('Norfolk Island (Australia)', 'Norfolk Island (Australia)'),
    ('North Korea', 'North Korea'),
    ('Northern Mariana Islands (USA)', 'Northern Mariana Islands (USA)'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Palestine', 'Palestine'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Pitcairn Islands (UK)', 'Pitcairn Islands (UK)'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Puerto Rico', 'Puerto Rico'),
    ('Qatar', 'Qatar'),
    ('Republic of the Congo', 'Republic of the Congo'),
    ('Reunion (France)', 'Reunion (France)'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Rwanda', 'Rwanda'),
    ('Saint Barthelemy (France)', 'Saint Barthelemy (France)'),
    ('Saint Helena, Ascension and Tristan da Cunha (UK)', 'Saint Helena, Ascension and Tristan da Cunha (UK)'),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
    ('Saint Lucia', 'Saint Lucia'),
    ('Saint Martin (France)', 'Saint Martin (France)'),
    ('Saint Pierre and Miquelon (France)', 'Saint Pierre and Miquelon (France)'),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tom and Principe', 'Sao Tom and Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', 'Senegal'),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Sint Maarten (Netherlands)', 'Sint Maarten (Netherlands)'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Korea', 'South Korea'),
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Svalbard and Jan Mayen (Norway)', 'Svalbard and Jan Mayen (Norway)'),
    ('Swaziland', 'Swaziland'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syria', 'Syria'),
    ('Taiwan', 'Taiwan'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania', 'Tanzania'),
    ('Thailand', 'Thailand'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tokelau (NZ)', 'Tokelau (NZ)'),
    ('Tonga', 'Tonga'),
    ('Trinidad and Tobago', 'Trinidad and Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Turks and Caicos Islands (UK)', 'Turks and Caicos Islands (UK)'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United States Virgin Islands (USA)', 'United States Virgin Islands (USA)'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Vatican City', 'Vatican City'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Wallis and Futuna (France)', 'Wallis and Futuna (France)'),
    ('Western Sahara', 'Western Sahara'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe'),
]
NOTIFICATION_PREFERENCE = [
    ('None', 'None'),
    ('Email', 'EMail'),
]


# ####################### Profile #######################
class Profile(models.Model):
    """Profile model for every user account. Also central to the model design.
    Child of Django's User Model (every Profile is associated with a User).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    pronoun = models.CharField(
        max_length=20,
        choices=PRONOUN_CHOICES,
        default='---',
    )
    spiritual_name = models.CharField(
        max_length=200,
        default='',
        unique=True,
        help_text='''Please enter the name you now identify with. 
        Where applicable this will be used as the name by which you are identified in Soul Synthesis.''',
    )
    bio = HTMLField(
        default='',
        blank=True,
        null=True,
        help_text='If moved, please share a little about yourself.',
    )
    given_first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='If moved, please enter the name you were given.',
    )
    given_last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='If moved, please enter your given last name (surname).',
    )
    address_1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='If moved, please enter your current address.',
    )
    address_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        help_text='Please enter the city (or town/village) you currently reside in.',
    )
    state_province_county = models.CharField(
        max_length=100,
        verbose_name='State/Province/County',
        help_text='Please identify the region (State/Province/County) you currently reside in.',
    )
    postal_zip_code = models.CharField(
        max_length=10,
        verbose_name='postal/zip code',
        blank=True,
        null=True,
        help_text='If moved, please enter the postal or zip code for your current address.',
    )
    country = models.CharField(
        max_length=100,
        choices=COUNTRY_CHOICES,
        default='---',
        help_text='Please select the country you currently reside in.',
    )
    phone = PhoneField(
        blank=True,
        null=True,
        help_text='If moved, please enter a contact phone number.',
    )
    notification_preference = models.CharField(
        max_length=10,
        choices=NOTIFICATION_PREFERENCE,
        default='None',
        help_text='''If you would like to receive automated notifications from Soul Synthesis please select your preference. You can change this setting at any time.'''
    )

    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.spiritual_name
