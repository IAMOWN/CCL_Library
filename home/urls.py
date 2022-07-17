from django.urls import path

from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('newsletter/<int:pk>/', views.NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('subscribe/', views.SubscriptionCreate.as_view(), name='subscribe'),
    path('confirm_subscription/<str:audience>/<str:email>/', views.subscription_confirm, name='confirm-subscription'),
]
