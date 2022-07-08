from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


# ####################### CONSTANTS #######################
BASE_URL = settings.DOMAIN


# ####################### DATE LOGIC #######################
def get_current_year():
    return datetime.now(tz=timezone.utc).year


# ####################### BASIC VIEWS #######################
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, prefix='user')
        profile_form = ProfileUpdateForm(request.POST, prefix='profile')
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been created. You can now log in.')
            return redirect('login')
    else:
        user_form = UserRegisterForm(prefix='user')
        profile_form = ProfileUpdateForm(prefix='profile')
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/register.html', context=context)


@login_required
def profile(request):
    user_profile_object = Profile.objects.get(user__username=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been successfully updated.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile_object,
        'year': get_current_year(),
    }
    return render(request, 'users/profile.html', context)


# ####################### PROFILE VIEWS #######################
class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Profile
    template_name = 'users/profiles.html'
    context_object_name = 'profiles'
    queryset = Profile.objects.all().order_by('spiritual_name')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Soul Synthesis Profiles'

        search_input = self.request.GET.get('search-area') or ''

        context['dear_souls'] = Profile.objects.all().order_by('spiritual_name')

        # ### SEARCH ###
        context['search_off'] = True
        if search_input:
            context['profiles'] = Profile.objects.get(spiritual_name=search_input)
            context['search_count'] = 1
            context['search_entered'] = search_input
            context['search_type'] = 'Spiritual'
            context['search_off'] = False

        return context


# ####################### Profile - Detail View #######################
class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'CCL_Library Profile'

        return context

