from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
# from django.db.models import Case, F, Q, Value, When, DateTimeField
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User

from .models import (
    Tag,
    Collection,
    CosmicAuthor,
    LibraryRecord,
    CollectionOrder,
    DiscourseSeries,
    ReadingProgress,
    LibraryObservation,
    RecordRead,
)

from .forms import (
    CreateTagForm,
    UpdateTagForm,
    CreateCollectionForm,
    UpdateCollectionForm,
    CreateDiscourseSeriesForm,
    UpdateDiscourseSeriesForm,
    CreateCosmicAuthorForm,
    UpdateCosmicAuthorForm,
    CreateLibraryRecordForm,
    UpdateLibraryRecordForm,
    CollectionRecordForm,
    CollectionRecordFormSet,
    CreateLibraryObservationForm,
)

from iamown.models import (
    Task,
    ServiceGroup,
    LEE,
)

from users.models import (
    Profile,
)

from ipware import get_client_ip


# ####################### CONSTANTS #######################
DOMAIN = settings.DOMAIN
FROM_EMAIL = settings.FROM_EMAIL
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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/Soul%20Synthesis%20Email%20Header.png" alt="Soul Synthesis email header banner" width: 600px;"/>
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
                                <img src="https://cdn.cosmicchrist.love/ccl-library-static/CCL_Library/Soul%20Synthesis%20Email%20Footer%20-%2072.png" alt="Whurthy email header banner" width: 600px;"/>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </body>
                    </html>
'''
LIBRARY_TASK_URL = 'https://cosmicchrist.love/tasks/library/'
SOUL_SYNTHESIS_S3_STORAGE = 'https://cloud.digitalocean.com/spaces/soul-synthesis-storage?i=1420f9'

LEE_TASK_RECORD_OBS_1 = 'Record Observation (1) Initial Review'
DIGITAL_LIBRARIAN_GROUP_NAME = 'Digital Librarians'
RECORD_READING_DURATION = 24  # Minutes before a new entry is added to RecordsRead: designed to prevent false refreshing

# ####################### FUNCTIONS #######################
def get_current_date():
    return datetime.now().date()


def get_current_datetime():
    # return datetime.now()
    return datetime.now(tz=timezone.utc)


def send_email(subject, to_email, message):
    send_mail(
        subject,
        message,
        FROM_EMAIL,
        [to_email],
        fail_silently=True,
        html_message=message,
    )


# ####################### TAG VIEWS #######################
class TagList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tag
    template_name = 'library/tags.html'
    context_object_name = 'tags'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Library Record Tags'

        return context


# ####################### Tag - Detail View #######################
class TagDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Tag
    template_name = 'library/tag_detail.html'
    context_object_name = 'tag'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Tag: {Tag.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Tag - Create View #######################
class TagCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = 'library/tag_form.html'
    reverse_lazy('tags')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.tag
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Tag "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Tag - Update View #######################
class TagUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    form_class = UpdateTagForm
    template_name = 'library/tag_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'
        return context


# ####################### Tag - Delete View #######################
class TagDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'library/tag_confirm_delete.html'
    success_url = reverse_lazy('tags')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        tag_to_delete = Tag.objects.get(pk=self.kwargs['pk'])
        records_with_tag = LibraryRecord.objects.filter(tags__tag=tag_to_delete)
        context['records_with_tag'] = records_with_tag
        context['records_with_tag_count'] = records_with_tag.count()

        return context


# ####################### COLLECTION VIEWS #######################
class CollectionList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Collection
    template_name = 'library/collections.html'
    context_object_name = 'collections'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Library Collections'

        return context


# ####################### Collection - Detail View #######################
class CollectionDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Collection
    template_name = 'library/collection_detail.html'
    context_object_name = 'collection'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Collection: {Collection.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Collection - Create View #######################
class CollectionCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Collection
    form_class = CreateCollectionForm
    template_name = 'library/collection_form.html'
    reverse_lazy('collections')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.collection
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Collection "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Collection - Update View #######################
class CollectionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Collection
    form_class = UpdateCollectionForm
    template_name = 'library/collection_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


# ####################### Collection - Delete View #######################
class CollectionDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Collection
    template_name = 'library/collection_confirm_delete.html'
    success_url = reverse_lazy('collections')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        collection_to_delete = Collection.objects.get(pk=self.kwargs['pk'])
        library_records_with_collection = []
        record_count = 0
        library_collection = CollectionOrder.objects.filter(collection__collection=collection_to_delete).order_by('order_number')
        for record in library_collection:
            library_records_with_collection.append(record.record)
            record_count += 1
        context['library_records_with_collection'] = library_records_with_collection
        context['library_records_with_collection_count'] = record_count
        context['collection_id'] = self.kwargs['pk']

        return context


# ####################### DISCOURSE SERIES VIEWS #######################
class DiscourseSeriesList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DiscourseSeries
    template_name = 'library/discourse_series.html'
    context_object_name = 'discourse_series'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Library Record Discourse Series Titles'

        return context


# ####################### Discourse Series - Detail View #######################
class DiscourseSeriesDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DiscourseSeries
    template_name = 'library/discourse_series_detail.html'
    context_object_name = 'discourse_series'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Discourse Series: {DiscourseSeries.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Discourse Series - Create View #######################
class DiscourseSeriesCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DiscourseSeries
    form_class = CreateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.discourse_series
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Discourse Series "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Discourse Series - Update View #######################
class DiscourseSeriesUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DiscourseSeries
    form_class = UpdateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


# ####################### Discourse Series - Delete View #######################
class DiscourseSeriesDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DiscourseSeries
    template_name = 'library/discourse_series_confirm_delete.html'
    success_url = reverse_lazy('discourse-series')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        series_to_delete = DiscourseSeries.objects.get(pk=self.kwargs['pk'])
        records_with_series = LibraryRecord.objects.filter(discourse_series__discourse_series=series_to_delete)
        context['records_with_series'] = records_with_series
        context['records_with_series_count'] = records_with_series.count()

        return context


# ####################### MASTERS (COSMIC AUTHOR) VIEWS #######################
class CosmicAuthorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CosmicAuthor
    template_name = 'library/masters.html'
    context_object_name = 'authors'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Masters'

        return context


# ####################### Master - Detail View #######################
class CosmicAuthorDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CosmicAuthor
    template_name = 'library/master_detail.html'
    context_object_name = 'author'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Master: {CosmicAuthor.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Master - Create View #######################
class CosmicAuthorCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CosmicAuthor
    form_class = CreateCosmicAuthorForm
    template_name = 'library/master_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        message = form.instance.author
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Cosmic Author "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Master - Update View #######################
class CosmicAuthorUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CosmicAuthor
    form_class = UpdateCosmicAuthorForm
    template_name = 'library/master_form.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


# ####################### Master - Delete View #######################
class CosmicAuthorDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CosmicAuthor
    template_name = 'library/master_confirm_delete.html'
    success_url = reverse_lazy('masters')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        master_to_delete = CosmicAuthor.objects.get(pk=self.kwargs['pk'])
        records_with_master = LibraryRecord.objects.filter(principal_cosmic_author__author=master_to_delete)
        records_with_supporting_master = LibraryRecord.objects.filter(supporting_cosmic_authors__author__icontains=master_to_delete)
        context['records_with_master'] = records_with_master
        context['records_with_master_count'] = records_with_master.count() + records_with_supporting_master.count()
        context['records_with_supporting_master'] = records_with_supporting_master

        return context


# ####################### LIBRARY RECORD VIEWS #######################
class LibraryRecordList(ListView):
    model = LibraryRecord
    template_name = 'library/library_records.html'
    context_object_name = 'library_records'

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Library Records'

        return context


# ####################### Library Record - Detail View #######################
class LibraryRecordDetail(DetailView):
    model = LibraryRecord
    template_name = 'library/library_record_detail.html'
    context_object_name = 'library_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.now().date()

        # Process Record Read update
        library_record = LibraryRecord.objects.get(id=self.kwargs['pk'])
        # Get IP Address
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip is None:
            ip_result = None
        else:  # There is an IP
            if is_routable:
                ip_result = True  # We got it
            else:
                ip_result = "Private"  # but it's private
        # Process records read
        if self.request.user.is_authenticated:
            # Check if record was previously marked as read within the last RECORD_READING_DURATION minutes
            reader = User.objects.get(id=self.request.user.id)
            time_to_check = get_current_datetime() - timedelta(minutes=RECORD_READING_DURATION)
            if RecordRead.objects.filter(record_read=library_record, date_read__gte=time_to_check, reader=reader).count() == 0:
                # Create entry in RecordRead model
                RecordRead.objects.create(
                    record_read=library_record,
                    reader=reader,
                    client_ip=client_ip,
                )
        else:
            # Add anonymous read + IP to Records Read
            RecordRead.objects.create(
                record_read=library_record,
                client_ip=client_ip,
            )

        # Build Collection metadata for record
        record_title = LibraryRecord.objects.get(id=self.kwargs['pk']).title
        record_in_collections = CollectionOrder.objects.filter(record__title=record_title).order_by('collection')
        collection_list_str = ''
        list_count = 0
        for record in record_in_collections:
            list_count += 1
            collection_list_str = collection_list_str + f'{record.collection.collection}; '
        context['collection_list_str'] = collection_list_str
        context['collection_list_count'] = list_count

        # Get Reading Progress for user's view of the record
        if self.request.user.is_authenticated:
            reading_progress_obj = ReadingProgress.objects.none()
            # Query for current reading progress: If it exists populate the dropdown or return a blank
            try:
                reading_progress_obj = ReadingProgress.objects.get(dear_soul__username=self.request.user, record_id=self.kwargs['pk'])
                current_reading_progress = reading_progress_obj.reading_progress
            except ReadingProgress.DoesNotExist:
                current_reading_progress = '---------'
            context['current_reading_progress'] = current_reading_progress
            selected_reading_progress = self.request.GET.get('reading-progress') or ''
            # Process authenticated user change of Reading Progress for record
            if current_reading_progress == '---------' and selected_reading_progress == '1) On Reading List':
                log_update = f'>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                new_reading_progress_obj = ReadingProgress(
                    dear_soul=self.request.user,
                    record_id=self.kwargs['pk'],
                    date_added=current_date,
                    reading_progress='1) On Reading List',
                    date_latest=current_date,
                    reading_progress_log=log_update
                )
                new_reading_progress_obj.save()
                context['current_reading_progress'] = '1) On Reading List'

            elif current_reading_progress == '---------' and selected_reading_progress == '2) Reading In Progress':
                log_update = f'>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                new_reading_progress_obj = ReadingProgress(
                    dear_soul=self.request.user,
                    record_id=self.kwargs['pk'],
                    date_added=current_date,
                    date_started=current_date,
                    reading_progress='2) Reading In Progress',
                    date_latest=current_date,
                    reading_progress_log=log_update
                )
                new_reading_progress_obj.save()
                context['current_reading_progress'] = '2) Reading In Progress'

            elif current_reading_progress == '---------' and selected_reading_progress == '3) Completed Reading':
                log_update = f'>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                new_reading_progress_obj = ReadingProgress(
                    dear_soul=self.request.user,
                    record_id=self.kwargs['pk'],
                    date_added=current_date,
                    date_started=current_date,
                    date_completed=current_date,
                    reading_progress='3) Completed Reading',
                    date_latest=current_date,
                    reading_progress_log=log_update,
                    total_readings = 1,
                )
                new_reading_progress_obj.save()
                context['current_reading_progress'] = '3) Completed Reading'

            elif current_reading_progress == '1) On Reading List' and selected_reading_progress == '2) Reading In Progress':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.date_started = current_date
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress = '2) Reading In Progress'
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.save(
                    update_fields=[
                        'date_started',
                        'reading_progress',
                        'date_latest',
                        'reading_progress_log',
                    ]
                )
                context['current_reading_progress'] = '2) Reading In Progress'

            elif current_reading_progress == '1) On Reading List' and selected_reading_progress == '3) Completed Reading':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.date_started = current_date
                reading_progress_obj.date_completed = current_date
                reading_progress_obj.reading_progress = '3) Completed Reading'
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.total_readings = reading_progress_obj.total_readings + 1
                reading_progress_obj.save(
                    update_fields=[
                        'date_completed',
                        'date_started',
                        'reading_progress',
                        'date_latest',
                        'reading_progress_log',
                        'total_readings',
                    ]
                )
                context['current_reading_progress'] = '3) Completed Reading'

            elif current_reading_progress == '2) Reading In Progress' and selected_reading_progress == '3) Completed Reading':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.date_completed = current_date
                reading_progress_obj.reading_progress = '3) Completed Reading'
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.total_readings = reading_progress_obj.total_readings + 1
                reading_progress_obj.save(
                    update_fields=[
                        'date_completed',
                        'reading_progress',
                        'date_latest',
                        'reading_progress_log',
                        'total_readings',
                    ]
                )
                context['current_reading_progress'] = '3) Completed Reading'

            elif current_reading_progress == '2) Reading In Progress' and selected_reading_progress == '1) On Reading List':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.reading_progress = '1) On Reading List'
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.save(
                    update_fields=[
                        'reading_progress',
                        'date_latest',
                        'reading_progress_log',
                    ]
                )
                context['current_reading_progress'] = '1) On Reading List'

            elif current_reading_progress == '3) Completed Reading' and selected_reading_progress == '1) On Reading List':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.reading_progress = '1) On Reading List'
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.save(
                    update_fields=[
                        'reading_progress',
                        'date_latest',
                        'reading_progress_log',
                    ]
                )
                context['current_reading_progress'] = '1) On Reading List'

            elif current_reading_progress == '3) Completed Reading' and selected_reading_progress == '2) Reading In Progress':
                log_update = f'{reading_progress_obj.reading_progress_log}<p>>>><em>Current</em> <strong>{current_reading_progress}</strong> <em>changed to</em> <strong>{selected_reading_progress}</strong> <em>on</em> <strong>{current_date}</strong>'
                reading_progress_obj.reading_progress = '2) Reading In Progress'
                reading_progress_obj.date_latest = current_date
                reading_progress_obj.reading_progress_log = log_update
                reading_progress_obj.save(update_fields=['reading_progress', 'date_latest', 'reading_progress_log'])
                context['current_reading_progress'] = '2) Reading In Progress'

        # Build previous and next record buttons
        libary_record = get_object_or_404(LibraryRecord, id=self.kwargs['pk'])
        if libary_record.discourse_series:
            # Build Series list
            series = LibraryRecord.objects.filter(discourse_series=libary_record.discourse_series).order_by('part_number')
            part_numbers = []
            for record in series:
                if record.part_number is not None:
                    part_numbers.append(record.part_number)
            # If there's only one record then remove the buttons displayed
            if len(part_numbers) == 1:
                context['series'] = False
            else:
                context['series'] = True
                if libary_record.part_number is None:
                    context['series'] = False
                else:
                    current_part_number = int(libary_record.part_number)
                    lowest_part_number = int(min(part_numbers))
                    # Check if there's a previous record in the series
                    if current_part_number > lowest_part_number:
                        context['previous_exists'] = True
                        try:
                            # Get the record id for the previous Discourse in the Series
                            context['previous'] = LibraryRecord.objects.get(discourse_series=libary_record.discourse_series, part_number=int(libary_record.part_number) - 1).id
                        except LibraryRecord.DoesNotExist:
                            # Or not
                            context['series'] = False
                    else:
                        context['previous_exists'] = False
                    highest_part_number = int(max(part_numbers))
                    if current_part_number < highest_part_number:
                        context['next_exists'] = True
                        try:
                            # Get the record id for the next Discourse in the Series
                            context['next'] = LibraryRecord.objects.get(discourse_series=libary_record.discourse_series, part_number=int(libary_record.part_number) + 1).id
                        except LibraryRecord.DoesNotExist:
                            # Or not
                            context['series'] = False
                    else:
                        context['next_exists'] = False
        else:
            context['series'] = False

        context['collection_orders'] = CollectionOrder.objects.filter(record=self.kwargs['pk'])

        return context


# ####################### Library Records - Books #######################
class BooksList(ListView):
    model = LibraryRecord
    template_name = 'library/records_filtered.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        library_record_type="Book"
    ).order_by('date_communicated')

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Books'
        context['page_type'] = 'Books'

        return context


# ####################### Library Records - Cosmic Review #######################
class CosmicReviewsList(ListView):
    model = LibraryRecord
    template_name = 'library/records_filtered.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        library_record_type="Cosmic Review"
    ).order_by('date_communicated')

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Cosmic Reviews'
        context['page_type'] = 'Cosmic Reviews'

        return context


# ####################### Library Records - Discourses #######################
class DiscoursesList(ListView):
    model = LibraryRecord
    template_name = 'library/records_filtered.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        library_record_type="Discourse"
    ).order_by('discourse_series', 'date_communicated')

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Discourses'
        context['page_type'] = 'Discourses'

        return context


# ####################### Library Records - Invocations #######################
class InvocationsList(ListView):
    model = LibraryRecord
    template_name = 'library/records_filtered.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        library_record_type="Invocation"
    ).order_by('date_communicated')

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Invocations'
        context['page_type'] = 'Invocations'

        return context


# ####################### Library Records - Petitions #######################
class PetitionsList(ListView):
    model = LibraryRecord
    template_name = 'library/records_filtered.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        library_record_type="Petition"
    ).order_by('date_communicated')

    paginate_by = 12
    ordering = 'date_communicated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EGA Petitions'
        context['page_type'] = 'Petitions'

        return context


# ####################### Library Records - Series: Boot Camp Alchemy Class  #######################
class SeriesBootCampList(ListView):
    model = LibraryRecord
    template_name = 'library/records_series_boot_camp.html'
    context_object_name = 'library_records'
    queryset = LibraryRecord.objects.filter(
        discourse_series__discourse_series='Boot Camp Alchemy Class'
    ).order_by('part_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Boot Camp Alchemy Class Discourse Series'
        context['page_type'] = 'Discourses'

        return context


# ####################### COLLECTIONS - True Constition #######################
class CollectionTrueConstitutionList(ListView):
    model = CollectionOrder
    template_name = 'library/records_collection_true_constitution.html'
    context_object_name = 'collection'
    paginate_by = 12
    ordering = 'date_communicated'

    # def get_queryset(self):
    #     return LibraryRecord.objects.filter(
    #         record_in_collection_order__collection__collection='True Constitution'
    #     ).order_by('record_in_collection_order__order_number')

    def get_queryset(self):
        return CollectionOrder.objects.filter(collection__collection='True Constitution').order_by('order_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add to Collection button
        library_records_in_collection = LibraryRecord.objects.none()
        if self.request.GET.get('add-to-reading-list'):
            collection = CollectionOrder.objects.filter(
                collection__collection='True Constitution'
            ).order_by('order_number')

            for item in collection:
                if not ReadingProgress.objects.filter(record_id=item.record.id, dear_soul=self.request.user).exists():
                    log_update = f'''
                    >>><strong>Record added to Reading List from the "True Constitution" Collection</strong> on 
                    {get_current_date()}'''
                    new_reading_progress_obj = ReadingProgress(
                        dear_soul=self.request.user,
                        record_id=item.record_id,
                        date_added=get_current_date(),
                        reading_progress='1) On Reading List',
                        date_latest=get_current_date(),
                        reading_progress_log=log_update
                    )
                    new_reading_progress_obj.save()

        context['title'] = "The True Constitution Collection"

        return context


# ####################### Library Records - Collection: ENACA #######################
class CollectionENACAList(ListView):
    model = CollectionOrder
    template_name = 'library/records_collection_ENACA.html'
    context_object_name = 'collection'
    paginate_by = 12

    def get_queryset(self):
        return CollectionOrder.objects.filter(collection__collection='ENACA').order_by('order_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add to Collection button
        library_records_in_collection = LibraryRecord.objects.none()
        if self.request.GET.get('add-to-reading-list'):
            collection = CollectionOrder.objects.filter(collection__collection='ENACA').order_by('order_number')

            for item in collection:
                if not ReadingProgress.objects.filter(record_id=item.record.id, dear_soul=self.request.user).exists():
                    log_update = f'''
                    >>><strong>Record added to Reading List from the "ENACA" Collection</strong> on 
                    {get_current_date()}'''
                    new_reading_progress_obj = ReadingProgress(
                        dear_soul=self.request.user,
                        record_id=item.record_id,
                        date_added=get_current_date(),
                        reading_progress='1) On Reading List',
                        date_latest=get_current_date(),
                        reading_progress_log=log_update
                    )
                    new_reading_progress_obj.save()

        context['title'] = 'The ENACA (Earth Nuclear And Chemical Affairs) Collection'

        return context


# ####################### Library Records - Collection: St Germain 'I AM' Freedom Alchemy Class #######################
class CollectionIAMFreedomList(ListView):
    model = CollectionOrder
    template_name = 'library/records_collection_IAM_FREEDOM.html'
    context_object_name = 'collection'
    paginate_by = 12

    def get_queryset(self):
        return CollectionOrder.objects.filter(
            collection__collection="St Germain 'I AM' Freedom Alchemy Class"
        ).order_by('order_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add to Collection button
        library_records_in_collection = LibraryRecord.objects.none()
        if self.request.GET.get('add-to-reading-list'):
            collection = CollectionOrder.objects.filter(
                collection__collection="St Germain 'I AM' Freedom Alchemy Class"
            ).order_by('order_number')

            for item in collection:
                if not ReadingProgress.objects.filter(
                        record_id=item.record.id,
                        dear_soul=self.request.user
                ).exists():
                    log_update = f'''
                    >>><strong>Record added to Reading List from the "St Germain 'I AM' Freedom Alchemy Class" 
                    Collection on </strong> {get_current_date()}.
                    '''
                    new_reading_progress_obj = ReadingProgress(
                        dear_soul=self.request.user,
                        record_id=item.record_id,
                        date_added=get_current_date(),
                        reading_progress='1) On Reading List',
                        date_latest=get_current_date(),
                        reading_progress_log=log_update
                    )
                    new_reading_progress_obj.save()

        context['title'] = "The St Germain 'I AM' Freedom Alchemy Class Collection"

        return context


# ####################### Library Records - Collection: GESARA #######################
class CollectionGESARAList(ListView):
    model = CollectionOrder
    template_name = 'library/records_collection_GESARA.html'
    context_object_name = 'collection'
    paginate_by = 12

    def get_queryset(self):
        return CollectionOrder.objects.filter(collection__collection="GESARA").order_by('order_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add to Collection button
        library_records_in_collection = LibraryRecord.objects.none()
        if self.request.GET.get('add-to-reading-list'):
            collection = CollectionOrder.objects.filter(collection__collection='GESARA').order_by('order_number')

            for item in collection:
                if not ReadingProgress.objects.filter(record_id=item.record.id, dear_soul=self.request.user).exists():
                    log_update = f'''
                    >>><strong>Record added to Reading List from the "GESARA" Collection</strong> on 
                    {get_current_date()}'''
                    new_reading_progress_obj = ReadingProgress(
                        dear_soul=self.request.user,
                        record_id=item.record_id,
                        date_added=get_current_date(),
                        reading_progress='1) On Reading List',
                        date_latest=get_current_date(),
                        reading_progress_log=log_update
                    )
                    new_reading_progress_obj.save()

        context['title'] = 'The GESARA (Global Economic Security and Reformation Act) Collection'

        return context


# ####################### Library Record - Create View #######################
class LibraryRecordCreate(LoginRequiredMixin, CreateView):
    model = LibraryRecord
    form_class = CreateLibraryRecordForm
    template_name = 'library/library_record_form.html'

    def form_valid(self, form):
        message = form.instance.title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Library Record "{message}" has been added'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context


# ####################### Library Record - Update View #######################
class LibraryRecordUpdate(LoginRequiredMixin, UpdateView):
    model = LibraryRecord
    form_class = UpdateLibraryRecordForm
    template_name = 'library/library_record_form.html'

    def form_valid(self, form):
        message = form.instance.title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Library Record "{message}" has been updated'
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Update'

        return context


# ####################### Library Record - Delete View #######################
class LibraryRecordDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LibraryRecord
    template_name = 'library/library_record_confirm_delete.html'
    success_url = reverse_lazy('library-records')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# ####################### SEARCH VIEW #######################
class SearchView(ListView):
    model = LibraryRecord
    template_name = 'library/search.html'
    context_object_name = 'library_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_on'] = False

        # Search inputs
        start_search_input = self.request.GET.get('start-date') or ''
        end_search_input = self.request.GET.get('end-date') or ''

        title_search_input = self.request.GET.get('title-search') or ''
        text_search_input = self.request.GET.get('text-search') or ''

        record_type_search_input = self.request.GET.get('record-type-search') or ''
        series_search_input = self.request.GET.get('series-search') or ''
        collection_search_input = self.request.GET.get('collection-search') or ''

        author_search_input = self.request.GET.get('author-search') or ''
        supporting_author_search_input = self.request.GET.get('supporting-author-search') or ''
        tags_search_input = self.request.GET.get('tag-search') or ''

        # TODO Add language search once records translated into other languages are added

        # Check for same date being entered into search - allows for search message to make sense
        search_error = False
        same_day_search = False
        if start_search_input == end_search_input:
            same_day_search = True

        # Search only between date range:
        if start_search_input and end_search_input and not record_type_search_input and not title_search_input and not author_search_input and not series_search_input and not supporting_author_search_input and not tags_search_input and not text_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = cleaned_start_search_input
                context['search_type'] = 'date'
                context['search_on'] = True
            else:
                search_error = True

        # Search only title
        elif not start_search_input and not end_search_input and title_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                title__icontains=title_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = title_search_input
            context['search_type'] = 'title'
            context['search_on'] = True
        # Search title and date
        elif start_search_input and end_search_input and title_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    title__icontains=title_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'with "{title_search_input}" in the title between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/title'
                context['search_on'] = True
            else:
                search_error = True

        # Search only text
        elif not start_search_input and not end_search_input and text_search_input and not record_type_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                text__icontains=text_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = text_search_input
            context['search_type'] = 'text'
            context['search_on'] = True
        # Search text and date
        elif start_search_input and end_search_input and text_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    text__icontains=text_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'with "{text_search_input}" in the text between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/text'
                context['search_on'] = True
            else:
                search_error = True

        # Search for record type:
        elif not start_search_input and not end_search_input and record_type_search_input and not text_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                library_record_type=record_type_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = record_type_search_input
            context['search_type'] = 'record type'
            context['search_on'] = True
        # Search record type and date
        elif start_search_input and end_search_input and record_type_search_input and not text_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    library_record_type=record_type_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'of the type "{record_type_search_input}" between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/record type'
                context['search_on'] = True
            else:
                search_error = True
        # Search for record type and text:
        elif not start_search_input and not end_search_input and record_type_search_input != 'Invocation' and text_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                library_record_type=record_type_search_input,
                text__icontains=text_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = f'for the record type {record_type_search_input} with the text "{text_search_input}"'
            context['search_type'] = 'record type/text'
            context['search_on'] = True
        # Search for "Invocation" record type and text:
        elif not start_search_input and not end_search_input and record_type_search_input == 'Invocation' and text_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                library_record_type=record_type_search_input,
                invocation__icontains=text_search_input,
            ).order_by('part_number')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = f'for the record type {record_type_search_input} with the text "{text_search_input}"'
            context['search_type'] = 'record type/text'
            context['search_on'] = True

        # Search for series:
        elif not start_search_input and not end_search_input and series_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                discourse_series__discourse_series=series_search_input,
            ).order_by('part_number', 'date_communicated',)
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = series_search_input
            context['search_type'] = 'series'
            context['search_on'] = True
        # Search series and date
        elif start_search_input and end_search_input and series_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    discourse_series__discourse_series=series_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated', 'date_communicated',)
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'from the series "{series_search_input}" between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/series'
                context['search_on'] = True
            else:
                search_error = True

        # Search for Collection:
        elif collection_search_input:
            # Query based on search parameters
            library_records = []
            collection_order_number = []
            record_count = 0
            library_collection = CollectionOrder.objects.filter(collection__collection=collection_search_input).order_by('order_number')
            for record in library_collection:
                collection_order_number.append(record.order_number)
                library_records.append(record.record)
                record_count += 1
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['collection_order_number'] = collection_order_number

            context['search_count'] = record_count
            context['search_entered'] = collection_search_input
            context['search_type'] = 'collection'
            context['search_on'] = True

        # Search for Master:
        elif not start_search_input and not end_search_input and author_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                principal_cosmic_author__author__iexact=author_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = author_search_input
            context['search_type'] = 'Master'
            context['search_on'] = True
        # Search Master and date
        elif start_search_input and end_search_input and author_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    principal_cosmic_author__author=author_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'from the Master "{author_search_input}" between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/Master'
                context['search_on'] = True
            else:
                search_error = True

        # Search for supporting author:
        elif not start_search_input and not end_search_input and supporting_author_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                supporting_cosmic_authors__author__exact=supporting_author_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = supporting_author_search_input
            context['search_type'] = 'supporting Master'
            context['search_on'] = True
        # Search supporting author and date
        elif start_search_input and end_search_input and supporting_author_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    supporting_cosmic_authors__author=supporting_author_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'including the supporting Master "{supporting_author_search_input}" between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/supporting Master'
                context['search_on'] = True
            else:
                search_error = True

        # Search for tag:
        elif not start_search_input and not end_search_input and tags_search_input:
            # Query based on search parameters
            library_records = LibraryRecord.objects.filter(
                tags__tag=tags_search_input,
            ).order_by('date_communicated')
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
            context['search_count'] = library_records.count()
            context['search_entered'] = tags_search_input
            context['search_type'] = 'tag'
            context['search_on'] = True
        # Search tag and date
        elif start_search_input and end_search_input and tags_search_input:
            # Check that start is before end
            if start_search_input <= end_search_input:
                # Clean search parameters so they display date only
                cleaned_start_search_input = start_search_input[0:10]
                cleaned_end_search_input = end_search_input[0:10]
                context['start_search_input'] = cleaned_start_search_input
                context['end_search_input'] = cleaned_end_search_input
                # Extend search end by 1 day so that same day search can work
                end_search_input = datetime.strptime(end_search_input, '%Y-%m-%d') + timedelta(days=1)
                # Query based on search parameters
                library_records = LibraryRecord.objects.filter(
                    tags__tag=tags_search_input,
                    date_communicated__gte=cleaned_start_search_input,
                    date_communicated__lte=cleaned_end_search_input,
                ).order_by('date_communicated')
                # Fill out remaining search context variables for presentation
                context['library_records'] = library_records
                context['search_count'] = library_records.count()
                context['search_entered'] = f'with the tag "{tags_search_input}" between {cleaned_start_search_input} and {cleaned_end_search_input}'
                context['search_type'] = 'date/tag'
                context['search_on'] = True
            else:
                search_error = True

        context['search_error'] = search_error

        context['series'] = DiscourseSeries.objects.all().order_by('discourse_series')
        context['authors'] = CosmicAuthor.objects.all().order_by('author')
        context['tags'] = Tag.objects.all().order_by('tag')
        context['collections'] = Collection.objects.all().order_by('collection')
        context['same_day_search'] = same_day_search

        context['title'] = 'Search the Library'

        return context


# ####################### Collection Record FormSets #######################
@login_required
def collection_records(request, pk):
    collection = Collection.objects.get(pk=pk)
    collection_records = CollectionOrder.objects.filter(collection=collection).order_by('order_number')
    form = CollectionRecordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            collection_record = form.save(commit=False)
            collection_record.collection = collection
            collection_record.save()
            return redirect('collection-record-detail', pk=collection_record.id)
        else:
            return render(request, 'library/partials/collection_record_form.html', {
                'form': form,
            })

    context = {
        'title':"Manage Collection",
        'collection': collection,
        'form': form,
        'collection_records': collection_records
    }
    return render(request, 'library/collection_record_create.html', context)


# Partial Collection Records views
@login_required
def collection_record_form(request):
    form = CollectionRecordForm()
    context = {
        "form": CollectionRecordForm
    }
    return render(request, "library/partials/collection_record_form.html", context=context)


# Detail view
@login_required
def collection_record_detail(request, pk):
    collection_record = CollectionOrder.objects.get(pk=pk)
    context = {
        'collection_record': collection_record,
    }
    return render(request, "library/partials/collection_record_detail.html", context)


# Delete view
@login_required
def collection_record_delete(request, pk):
    collection_record = get_object_or_404(CollectionOrder, pk=pk)
    collection_record.delete()
    return HttpResponse("")


# Update view
@login_required
def collection_record_update(request, pk):
    collection_record = CollectionOrder.objects.get(pk=pk)
    collection = Collection.objects.get(collection=collection_record.collection)
    form = CollectionRecordForm(request.POST or None, instance=collection_record)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('collection-record-detail', pk=collection.id)

    context = {
        "form": form,
        'collection_record': collection_record,
        'collection': collection,
    }
    return render(request, "library/partials/collection_record_form.html", context)


# ####################### READING LIST VIEWS #######################
class ReadingList(LoginRequiredMixin, ListView):
    model = ReadingProgress
    template_name = 'library/reading_list.html'
    context_object_name = 'reading_progress'
    paginate_by = 12

    def get_queryset(self):
        return ReadingProgress.objects.filter(dear_soul__username=self.request.user).order_by(
            'reading_progress',
            'date_latest',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_on'] = False

        # Search inputs
        author_search_input = self.request.GET.get('author-search') or ''
        series_search_input = self.request.GET.get('series-search') or ''
        collection_search_input = self.request.GET.get('collection-search') or ''

        # Search for Master:
        if author_search_input:
            # Query based on search parameters
            refined_reading_list = ReadingProgress.objects.filter(
                record__principal_cosmic_author__author=author_search_input,
                dear_soul__username=self.request.user,
            ).order_by(
                'reading_progress',
                'date_latest',
            )

            # Fill out remaining search context variables for presentation
            context['refined_reading_list'] = refined_reading_list
            context['search_count'] = refined_reading_list.count()
            context['search_entered'] = author_search_input
            context['search_type'] = 'Master'
            context['search_on'] = True

        # Search for series:
        elif series_search_input:
            # Query based on search parameters
            refined_reading_list = ReadingProgress.objects.filter(
                record__discourse_series__discourse_series=series_search_input,
                dear_soul__username=self.request.user,
            ).order_by(
                'reading_progress',
                'date_latest',
            )
            # Fill out remaining search context variables for presentation
            context['refined_reading_list'] = refined_reading_list
            context['search_count'] = refined_reading_list.count()
            context['search_entered'] = series_search_input
            context['search_type'] = 'Series'
            context['search_on'] = True

        # Search for Collection:
        elif collection_search_input:
            # Query based on search parameters
            refined_reading_list = []
            collection_list = []
            record_count = 0
            library_collection_title_list = CollectionOrder.objects.filter(
                collection__collection=collection_search_input,
            ).values_list('record__title', flat=True).order_by('order_number')
            refined_reading_list = ReadingProgress.objects.filter(dear_soul__username=self.request.user, record__title__in=[library_collection_title_list])
            context['refined_reading_list'] = refined_reading_list
            context['search_count'] = refined_reading_list.count()
            context['search_entered'] = collection_search_input
            context['search_type'] = 'Collection'
            context['search_on'] = True

        context['series'] = DiscourseSeries.objects.all().order_by('discourse_series')
        context['authors'] = CosmicAuthor.objects.all().order_by('author')
        context['collections'] = Collection.objects.all().order_by('collection')

        # Query for user's reading list and sort by the date/progress
        reading_progress = ReadingProgress.objects.filter(dear_soul__username=self.request.user).order_by(
            'reading_progress',
            'date_latest',
        )

        # Non working conditional annotate()
        # reading_progress = ReadingProgress.objects.filter(dear_soul__username=self.request.user)\
        #     .annotate(
        #     date_to_display=Case(
        #         When(reading_progress='1) On Reading List', then=F('date_added')),
        #         When(reading_progress='2) Reading In Progress', then=F('date_started')),
        #         When(reading_progress='3) Completed Reading', then=F('date_completed')),
        #     ),
        #     output_field=DateTimeField(),
        # ).order_by(
        #     'date_to_display',
        # )

        # if reading_progress:
        if reading_progress.exists():
            context['records_exist'] = True
        else:
            context['records_exist'] = False

        context['title'] = 'Reading List'

        return context


# ####################### Reading List - Delete View #######################
class ReadingListItemDelete(LoginRequiredMixin, DeleteView):
    model = ReadingProgress
    template_name = 'library/reading_list_confirm_delete.html'
    success_url = '/reading_list/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Reading List Item'

        return context

    def form_valid(self, form):
        record_obj = ReadingProgress.objects.get(id=self.kwargs['pk'])
        record_title = record_obj.record.title
        record_type = record_obj.record.library_record_type
        record_type = record_obj.record.library_record_type
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The {record_type}, "{record_title}" has been removed from your Reading List.'
        )
        return super().form_valid(form)


# ####################### Record Observation #######################
class ObervationCreate(LoginRequiredMixin, CreateView):
    model = LibraryObservation
    form_class = CreateLibraryObservationForm
    template_name = 'library/observation_form.html'

    def form_valid(self, form):
        record = LibraryRecord.objects.get(id=self.kwargs['pk'])

        observer_obj = Profile.objects.get(user__username=self.request.user)
        observer = observer_obj.spiritual_name

        service_group = ServiceGroup.objects.get(service_group=DIGITAL_LIBRARIAN_GROUP_NAME)
        observation_type = form.instance.observation_type
        history_log = f'''>>> <strong>{observation_type} Library Observation</strong> >>> submitted by <strong>{observer}</strong> on <strong>{get_current_date()}</strong>'''
        form.instance.observer = observer_obj

        if observation_type == 'Typo':
            observed_typo = form.instance.typo
            suggested_correction = form.instance.suggested_correction
            form.instance.library_record = record
            self.object = form.save()
            observation_obj = LibraryObservation.objects.get(id=self.object.id)

            task_description = LEE.objects.get(task_name=LEE_TASK_RECORD_OBS_1).process_description + f'''
            Record: <a href="{DOMAIN}library_record/{record.id}/" class="text-CCL-Blue" target="_blank">{record.title}</a><br>
            Observer: {observer}<br>
            Observation type: {observation_type}<p>
            <strong>Typo: </strong>{form.instance.typo}<br>
            <strong>Suggested Correction: </strong>{form.instance.suggested_correction}'''

            Task.objects.create(
                task_title=f'Record Observation - {observation_type} made by {observer}',
                task_type='Library Observation',
                task_description=task_description,
                task_history_log=history_log,
                assigned_service_group=service_group,
                library_record=record,
                library_observation=observation_obj,
                book_urls_for_record=record.book_urls,
            )
        elif observation_type == 'Image':
            form.instance.library_record = record
            image_observation = form.instance.image_observation
            self.object = form.save()
            observation_obj = LibraryObservation.objects.get(id=self.object.id)
            task_description = LEE.objects.get(task_name=LEE_TASK_RECORD_OBS_1).process_description + f'''
            Record: <a href="{DOMAIN}library_record/{record.id}/" class="text-CCL-Blue" target="_blank">{record.title}</a><br>
            Observer: {observer}<br>
            Observation type: {observation_type}<p>
            <strong>Missing image comments: </strong>{image_observation}<br>'''

            Task.objects.create(
                task_title=f'Record Observation - {observation_type} made by {observer}',
                task_type='Library Observation',
                task_description=task_description,
                task_history_log=history_log,
                assigned_service_group=service_group,
                library_observation=observation_obj,
                book_urls_for_record=record.book_urls,
                library_record=record,
            )
        elif observation_type == 'Broken Link':
            form.instance.library_record = record
            link_observation = form.instance.link_observation
            self.object = form.save()
            observation_obj = LibraryObservation.objects.get(id=self.object.id)
            task_description = LEE.objects.get(task_name=LEE_TASK_RECORD_OBS_1).process_description + f'''
            Record: <a href="{DOMAIN}library_record/{record.id}/" class="text-CCL-Blue" target="_blank">{record.title}</a><br>
            Observer: {observer}<br>
            Observation type: {observation_type}<p>
            <strong>Broken link comments: </strong>{link_observation}<br>'''

            Task.objects.create(
                task_title=f'Record Observation - {observation_type} made by {observer}',
                task_type='Library Observation',
                task_description=task_description,
                task_history_log=history_log,
                assigned_service_group=service_group,
                library_observation=observation_obj,
                book_urls_for_record=record.book_urls,
                library_record=record,
            )
        elif observation_type == 'Other':
            form.instance.library_record = record
            general_observation = form.instance.general_observation
            self.object = form.save()
            observation_obj = LibraryObservation.objects.get(id=self.object.id)
            task_description = LEE.objects.get(task_name=LEE_TASK_RECORD_OBS_1).process_description + f'''
            Record: <a href="{DOMAIN}library_record/{record.id}/" class="text-CCL-Blue" target="_blank">{record.title}</a><br>
            Observer: {observer}<br>
            Observation type: {observation_type}<p>
            <strong>General observations: </strong>{general_observation}<br>'''

            Task.objects.create(
                task_title=f'Record Observation - {observation_type} made by {observer}',
                task_type='Library Observation',
                task_description=task_description,
                task_history_log=history_log,
                assigned_service_group=service_group,
                library_observation=observation_obj,
                book_urls_for_record=record.book_urls,
                library_record=record,
            )

        digital_librarians = User.objects.filter(groups__name=DIGITAL_LIBRARIAN_GROUP_NAME)
        for librarian in digital_librarians:
            if librarian.profile.notification_preference == 'Email':
                email_address = librarian.email
                email_subject = f'[CCL] A Record Observation has been submitted by {observer}'
                email_message = f"""
                {EMAIL_MESSAGE_1}
                Beloved {librarian.profile.spiritual_name},<p>
                {observer} has submitted a "{observation_type}" Library Observation.<p> 
                Please review the <a href='{LIBRARY_TASK_URL}'>Library Tasks</a> at your earliest convenience.<p>
                Note: It is possible that another Librarian may respond to this task before you do. When reviewing the task 
                be sure to check the task status as well as the Assigned Dear Soul for the task.<p>
                Love and Blessings
                {EMAIL_MESSAGE_2}
                """
                send_email(email_subject, email_address, email_message)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Beloved {observer}, your "{observation_type}" observation has been submitted and will be seen to by the Circle of Digital Librarians. Love and Blessings.',
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Create'

        return context
