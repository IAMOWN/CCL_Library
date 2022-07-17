from django.urls import path

from .views import (
    contact,
    newsletter,
    # NewsletterDetailView,
    SubscriptionCreate,
    subscription_confirm,
)

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('newsletter/', newsletter, name='newsletter'),
    # path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('subscribe/', SubscriptionCreate.as_view(), name='subscribe'),
    path('confirm_subscription/<str:audience>/<str:email>/', subscription_confirm, name='confirm-subscription'),
]
