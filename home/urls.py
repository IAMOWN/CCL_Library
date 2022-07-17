from django.urls import path

from home import views as home_views

urlpatterns = [
    path('contact/', home_views.contact, name='contact'),
    path('newsletter/', home_views.newsletter, name='newsletter'),
    path('newsletter/<int:pk>/', home_views.NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('subscribe/', home_views.SubscriptionCreate.as_view(), name='subscribe'),
    path('confirm_subscription/<str:audience>/<str:email>/', home_views.subscription_confirm, name='confirm-subscription'),
]
