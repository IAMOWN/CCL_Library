from datetime import datetime, timezone, timedelta

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

from library.models import (
    ReadingProgress,
    RecordRead,
)


# ####################### CONSTANTS #######################
BASE_URL = settings.DOMAIN


# ####################### DATE LOGIC #######################
def get_current_year():
    return datetime.now(tz=timezone.utc).year


def get_current_datetime():
    return datetime.now(tz=timezone.utc)


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
            messages.success(request, 'Your profile has been successfully updated.')
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
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Soul Synthesis Profiles'
        dear_souls = Profile.objects.all().order_by('spiritual_name')
        context['dear_souls'] = dear_souls

        # Process Reading Progress list and Records Read
        records_read_last_7 = []
        minus_days_7 = get_current_datetime() - timedelta(days=7)
        records_read_last_91 = []
        minus_days_91 = get_current_datetime() - timedelta(days=91)
        records_read_all = []
        reading_progress_by_profile_count = []
        for profile in dear_souls:
            reading_progress_by_profile_count.append(ReadingProgress.objects.filter(dear_soul__profile=profile).count())
            user = profile.user
            records_read_last_7.append(RecordRead.objects.filter(reader=user, date_read__gte=minus_days_7).count())
            records_read_last_91.append(RecordRead.objects.filter(reader=user, date_read__gte=minus_days_91).count())
            records_read_all.append(RecordRead.objects.filter(reader=user).count())
        context['reading_progress_by_profile_count'] = reading_progress_by_profile_count
        context['records_read_last_7'] = records_read_last_7
        context['records_read_last_91'] = records_read_last_91
        context['records_read_all'] = records_read_all

        # ### SEARCH ###
        search_input = self.request.GET.get('search-area') or ''
        context['search_off'] = True
        if search_input:
            context['profiles'] = Profile.objects.filter(spiritual_name=search_input)
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
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = Profile.objects.get(id=self.kwargs["pk"])
        user_obj = User.objects.get(id=self.kwargs['user_id'])
        context['user_id'] = self.kwargs['user_id']

        # Process Reading Progress list and Records Read
        reading_list = ReadingProgress.objects.filter(dear_soul__username=user_obj.username)
        context['reading_list'] = reading_list
        context['reading_list_count'] = reading_list.count()
        records_read_last_1 = 0
        minus_days_1 = get_current_datetime() - timedelta(days=1)
        records_read_last_7 = 0
        minus_days_7 = get_current_datetime() - timedelta(days=7)
        records_read_last_30 = 0
        minus_days_30 = get_current_datetime() - timedelta(days=30)
        records_read_last_91 = 0
        minus_days_91 = get_current_datetime() - timedelta(days=91)
        records_read_last_365 = 0
        minus_days_365 = get_current_datetime() - timedelta(days=365)
        records_read_all = []
        reading_progress_by_profile_count = 0
        user = self.request.user
        records_read_last_1 = RecordRead.objects.filter(reader=user, date_read__gte=minus_days_1).count()
        records_read_last_7 = RecordRead.objects.filter(reader=user, date_read__gte=minus_days_7).count()
        records_read_last_30 = RecordRead.objects.filter(reader=user, date_read__gte=minus_days_30).count()
        records_read_last_91 = RecordRead.objects.filter(reader=user, date_read__gte=minus_days_91).count()
        records_read_last_365 = RecordRead.objects.filter(reader=user, date_read__gte=minus_days_365).count()
        records_read_all = RecordRead.objects.filter(reader=user).count()
        context['records_read_last_1'] = records_read_last_1
        context['records_read_last_7'] = records_read_last_7
        context['records_read_last_30'] = records_read_last_30
        context['records_read_last_91'] = records_read_last_91
        context['records_read_last_365'] = records_read_last_365
        context['records_read_all'] = records_read_all

        return context
