from django.urls import path
from django.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from users import views as user_views
import users.views

from home import views

urlpatterns = [
    # Functional routes
    path('tinymce/', include('tinymce.urls')),

    # Admin/Auth routes
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', user_views.profile, name='profile'),

    # Admin
    path('love/', admin.site.urls),
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('love/', include(admin.site.urls)),

    # App includes
    path('', include('home.urls')),
    path('', include('iamown.urls')),
    path('', include('library.urls')),

    # Core routes
    path('', views.home, name='home'),
    path('training/', views.training, name='training'),
    path('librarian-training/', views.librarian_training, name='librarian-training'),
    path('release-notes/', views.release_notes, name='release-notes'),

    # User Profile
    path('profiles/', users.views.ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>/<int:user_id>/', user_views.ProfileDetailView.as_view(), name='profile-dear-soul'),
]
