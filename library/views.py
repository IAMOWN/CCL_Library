from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponse
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Tag,
    Collection,
    CosmicAuthor,
    LibraryRecord,
    CollectionOrder,
    DiscourseSeries,
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
)


# FUNCTIONS
def get_current_year():
    return datetime.now().year


# ####################### TAG VIEWS #######################
class TagList(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'library/tags.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Record Tags'

        return context


# ####################### Tag - Detail View #######################
class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'library/tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Tag: {Tag.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Tag - Create View #######################
class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = 'library/tag_form.html'
    reverse_lazy('tags')

    def form_valid(self, form):
        message = form.instance.tag
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Tag "{message}" has been added'
        )
        return super(TagCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TagCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Tag - Update View #######################
class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = UpdateTagForm
    template_name = 'library/tag_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TagUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

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
        context = super(TagDelete, self).get_context_data(**kwargs)

        tag_to_delete = Tag.objects.get(pk=self.kwargs['pk'])
        records_with_tag = LibraryRecord.objects.filter(tags__tag=tag_to_delete)
        context['records_with_tag'] = records_with_tag
        context['records_with_tag_count'] = records_with_tag.count()
        context['year'] = get_current_year()

        return context


# ####################### COLLECTION VIEWS #######################
class CollectionList(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'library/collections.html'
    context_object_name = 'collections'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Collections'

        return context


# ####################### Collection - Detail View #######################
class CollectionDetail(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'library/collection_detail.html'
    context_object_name = 'collection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Collection: {Collection.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Collection - Create View #######################
class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CreateCollectionForm
    template_name = 'library/collection_form.html'
    reverse_lazy('collections')

    def form_valid(self, form):
        message = form.instance.collection
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Collection "{message}" has been added'
        )
        return super(CollectionCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Collection - Update View #######################
class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = UpdateCollectionForm
    template_name = 'library/collection_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

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
        context = super(CollectionDelete, self).get_context_data(**kwargs)

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
        context['year'] = get_current_year()

        return context


# ####################### DISCOURSE SERIES VIEWS #######################
class DiscourseSeriesList(LoginRequiredMixin, ListView):
    model = DiscourseSeries
    template_name = 'library/discourse_series.html'
    context_object_name = 'discourse_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Record Discourse Series Titles'

        return context


# ####################### Discourse Series - Detail View #######################
class DiscourseSeriesDetail(LoginRequiredMixin, DetailView):
    model = DiscourseSeries
    template_name = 'library/discourse_series_detail.html'
    context_object_name = 'discourse_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Discourse Series: {DiscourseSeries.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Discourse Series - Create View #######################
class DiscourseSeriesCreate(LoginRequiredMixin, CreateView):
    model = DiscourseSeries
    form_class = CreateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def form_valid(self, form):
        message = form.instance.discourse_series
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Discourse Series "{message}" has been added'
        )
        return super(DiscourseSeriesCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(DiscourseSeriesCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Discourse Series - Update View #######################
class DiscourseSeriesUpdate(LoginRequiredMixin, UpdateView):
    model = DiscourseSeries
    form_class = UpdateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DiscourseSeriesUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

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
        context = super(DiscourseSeriesDelete, self).get_context_data(**kwargs)

        series_to_delete = DiscourseSeries.objects.get(pk=self.kwargs['pk'])
        records_with_series = LibraryRecord.objects.filter(discourse_series__discourse_series=series_to_delete)
        context['records_with_series'] = records_with_series
        context['records_with_series_count'] = records_with_series.count()
        context['year'] = get_current_year()

        return context


# ####################### MASTERS (COSMIC AUTHOR) VIEWS #######################
class CosmicAuthorList(LoginRequiredMixin, ListView):
    model = CosmicAuthor
    template_name = 'library/masters.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Masters'

        return context


# ####################### Master - Detail View #######################
class CosmicAuthorDetail(LoginRequiredMixin, DetailView):
    model = CosmicAuthor
    template_name = 'library/master_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Master: {CosmicAuthor.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Master - Create View #######################
class CosmicAuthorCreate(LoginRequiredMixin, CreateView):
    model = CosmicAuthor
    form_class = CreateCosmicAuthorForm
    template_name = 'library/master_form.html'

    def form_valid(self, form):
        message = form.instance.author
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Cosmic Author "{message}" has been added'
        )
        return super(CosmicAuthorCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CosmicAuthorCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Master - Update View #######################
class CosmicAuthorUpdate(LoginRequiredMixin, UpdateView):
    model = CosmicAuthor
    form_class = UpdateCosmicAuthorForm
    template_name = 'library/master_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CosmicAuthorUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

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
        context = super(CosmicAuthorDelete, self).get_context_data(**kwargs)

        master_to_delete = CosmicAuthor.objects.get(pk=self.kwargs['pk'])
        records_with_master = LibraryRecord.objects.filter(principal_cosmic_author__author=master_to_delete)
        records_with_supporting_master = LibraryRecord.objects.filter(supporting_cosmic_authors__author__icontains=master_to_delete)
        context['records_with_master'] = records_with_master
        context['records_with_master_count'] = records_with_master.count() + records_with_supporting_master.count()
        context['records_with_supporting_master'] = records_with_supporting_master
        context['year'] = get_current_year()

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
        context['year'] = get_current_year()
        context['title'] = 'Library Records'

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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()
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
        context['year'] = get_current_year()
        context['title'] = 'EGA Petition'
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
        context['year'] = get_current_year()
        context['title'] = 'Boot Camp Alchemy Class Discourse Series'
        context['page_type'] = 'Discourses'

        return context


# ####################### Library Records - Collection: ENACA #######################
class CollectionENACAList(ListView):
    model = LibraryRecord
    template_name = 'library/records_collection_ENACA.html'
    context_object_name = 'library_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        library_records = []
        library_collection = CollectionOrder.objects.filter(collection__collection='ENACA').order_by('order_number')
        for record in library_collection:
            library_records.append(record.record)
        context['library_records'] = library_records

        context['year'] = get_current_year()
        context['title'] = 'ENACA (Earth Nuclear And Chemical Affairs)'

        return context


# ####################### Library Records - Collection: St Germain 'I AM' Freedom Alchemy Class #######################
class CollectionIAMFreedomList(ListView):
    model = LibraryRecord
    template_name = 'library/records_collection_IAM_FREEDOM.html'
    context_object_name = 'library_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        library_records = []
        library_collection = CollectionOrder.objects.filter(collection__collection="St Germain 'I AM' Freedom Alchemy Class").order_by('order_number')
        for record in library_collection:
            library_records.append(record.record)
        context['library_records'] = library_records

        context['year'] = get_current_year()
        context['title'] = "St Germain 'I AM' Freedom Alchemy Class"

        return context


# ####################### Library Records - Collection: GESARA #######################
class CollectionGESARAList(ListView):
    model = LibraryRecord
    template_name = 'library/records_collection_GESARA.html'
    context_object_name = 'library_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        library_records = []
        library_collection = CollectionOrder.objects.filter(collection__collection='GESARA').order_by('order_number')
        for record in library_collection:
            library_records.append(record.record)
        context['library_records'] = library_records

        context['year'] = get_current_year()
        context['title'] = 'GESARA (Global Economic Security and Reformation Act)'

        return context


# ####################### Library Record - Detail View #######################
class LibraryRecordDetail(DetailView):
    model = LibraryRecord
    template_name = 'library/library_record_detail.html'
    context_object_name = 'library_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()

        # Build record ids for previous and next
        libary_record = get_object_or_404(LibraryRecord, id=self.kwargs['pk'])
        if libary_record.discourse_series:
            series = LibraryRecord.objects.filter(discourse_series=libary_record.discourse_series).order_by('part_number')
            part_numbers = []
            for record in series:
                part_numbers.append(record.part_number)
            if len(part_numbers) == 1:
                previous_exists = False
                next_exists = False
                context['series'] = False
                context['previous_exists'] = False
                context['next_exists'] = False
            else:
                context['series'] = True
                if libary_record.part_number > min(part_numbers):
                    context['previous_exists'] = True
                    previous = LibraryRecord.objects.get(discourse_series=libary_record.discourse_series, part_number=int(libary_record.part_number) - 1).id
                    print(f'previous: {previous}')
                    if previous is None:
                        context['previous'] = previous
                    else:
                        context['previous_exists'] = False
                else:
                    context['previous_exists'] = False
                if libary_record.part_number < max(part_numbers):
                    context['next_exists'] = True
                    next = LibraryRecord.objects.get(discourse_series=libary_record.discourse_series, part_number=int(libary_record.part_number) + 1).id
                    print(f'next: {next}')
                    if next is None:
                        context['next'] = next
                    else:
                        context['next_exists'] = False
                else:
                    context['next_exists'] = False
        else:
            context['series'] = False

        context['title'] = libary_record
        context['collection_orders'] = CollectionOrder.objects.filter(record=self.kwargs['pk'])

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
        return super(LibraryRecordCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryRecordCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

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
        return super(LibraryRecordUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryRecordUpdate, self).get_context_data(**kwargs)

        context['TINY_API'] = settings.TINY_API
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

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
        context = super(LibraryRecordDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

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
            record_count = 0
            library_collection = CollectionOrder.objects.filter(collection__collection=collection_search_input).order_by('order_number')
            for record in library_collection:
                library_records.append(record.record)
                record_count += 1
            # Fill out remaining search context variables for presentation
            context['library_records'] = library_records
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

        context['year'] = get_current_year()
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
