from django import forms
from django.forms.models import inlineformset_factory

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import (
    Tag,
    Collection,
    CosmicAuthor,
    LibraryRecord,
    CollectionOrder,
    DiscourseSeries,
    LibraryObservation,
)

from users.models import User


# ############ Tag form validation logic ############
def tag_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('tag') is None:
        form.add_error(
            'tag',
            'A tag must be entered.'
        )
    return


# ############ Collection form validation logic ############
def collection_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('collection') is None:
        form.add_error(
            'collection',
            'A collection must be entered.'
        )
    return


# ############ Discourse Series form validation logic ############
def discourse_series_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('discourse_series') is None:
        form.add_error(
            'discourse_series',
            'A discourse series title must be entered.'
        )
    return


# ############ Cosmic Author form validation logic ############
def cosmic_author_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('author') is None:
        form.add_error(
            'author',
            'An author must be entered.'
        )
    return


# ############ Library Record form validation logic ############
def library_record_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('title') is None:
        form.add_error(
            'title',
            'A title must be entered.'
        )
    if cleaned_data.get('text') is None:
        form.add_error(
            'text',
            'Text must be entered.'
        )
    if cleaned_data.get('date_communicated') is None:
        form.add_error(
            'date_communicated',
            'A date must be entered.'
        )
    return


# ############ Library Observation form validation logic ############
def library_observation_form_validation(form, form_type):
    cleaned_data = super(form_type, form).clean()
    if cleaned_data.get('observation_type') is None:
        form.add_error(
            'observation_type',
            'An observation type must be selected.'
        )
    return


# ####################### Create Tag Form #######################
class CreateTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = [
            'tag',
        ]

    def clean(self):
        tag_form_validation(self, CreateTagForm)
        return self.cleaned_data


# ####################### Update Tag Form #######################
class UpdateTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = [
            'tag',
        ]

    def clean(self):
        tag_form_validation(self, UpdateTagForm)
        return self.cleaned_data


# ####################### Create Collection Form #######################
class CreateCollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = [
            'collection',
        ]

    def clean(self):
        collection_form_validation(self, CreateCollectionForm)
        return self.cleaned_data


# ####################### Update Collection Form #######################
class UpdateCollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = [
            'collection',
        ]

    def clean(self):
        collection_form_validation(self, UpdateCollectionForm)
        return self.cleaned_data


# ####################### Create Discourse Series Form #######################
class CreateDiscourseSeriesForm(forms.ModelForm):

    class Meta:
        model = DiscourseSeries
        fields = [
            'discourse_series',
        ]

    def clean(self):
        discourse_series_form_validation(self, CreateDiscourseSeriesForm)
        return self.cleaned_data


# ####################### Update Discourse Series Form #######################
class UpdateDiscourseSeriesForm(forms.ModelForm):

    class Meta:
        model = DiscourseSeries
        fields = [
            'discourse_series',
        ]

    def clean(self):
        discourse_series_form_validation(self, UpdateDiscourseSeriesForm)
        return self.cleaned_data


# ####################### Create Cosmic Author Form #######################
class CreateCosmicAuthorForm(forms.ModelForm):

    class Meta:
        model = CosmicAuthor
        fields = [
            'author',
        ]

    def clean(self):
        cosmic_author_form_validation(self, CreateCosmicAuthorForm)
        return self.cleaned_data


# ####################### Update Cosmic Author Form #######################
class UpdateCosmicAuthorForm(forms.ModelForm):

    class Meta:
        model = CosmicAuthor
        fields = [
            'author',
        ]

    def clean(self):
        cosmic_author_form_validation(self, UpdateCosmicAuthorForm)
        return self.cleaned_data


# ####################### Create Library Record Form #######################
class CreateLibraryRecordForm(forms.ModelForm):

    class Meta:
        model = LibraryRecord
        fields = [
            'library_record_type',
            'title',
            'part_number',
            'discourse_series',
            'invocation',
            'text',
            'benediction',
            'principal_cosmic_author',
            'supporting_cosmic_authors',
            'tags',
            'language',
            'date_communicated',
            'pdf_url',
            'doc_url',
            'mp3_url',
        ]
        widgets = {
            'date_communicated': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        library_record_form_validation(self, CreateLibraryRecordForm)
        return self.cleaned_data


# ####################### Update Library Record Form #######################
class UpdateLibraryRecordForm(forms.ModelForm):

    class Meta:
        model = LibraryRecord
        fields = [
            'library_record_type',
            'title',
            'part_number',
            'discourse_series',
            'invocation',
            'text',
            'benediction',
            'principal_cosmic_author',
            'supporting_cosmic_authors',
            'tags',
            'language',
            'date_communicated',
            'pdf_url',
            'doc_url',
            'mp3_url',
        ]
        widgets = {
            'date_communicated': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean(self):
        library_record_form_validation(self, UpdateLibraryRecordForm)
        return self.cleaned_data


# ####################### DYNAMIC FORMSET - COLLECTION ORDER #######################
class CollectionRecordForm(forms.ModelForm):
    class Meta:
        model = CollectionOrder
        fields = [
            'record',
            'order_number',
        ]


CollectionRecordFormSet = inlineformset_factory(
    Collection,
    CollectionOrder,
    CollectionRecordForm,
    can_delete=True,
    min_num=1,
    extra=1,
    max_num=99,
)


# ####################### Create Library Observation Form #######################
class CreateLibraryObservationForm(forms.ModelForm):

    class Meta:
        model = LibraryObservation
        fields = [
            'observation_type',
            'observer',
            'typo',
            'suggested_correction',
            'image_observation',
            'link_observation',
            'header_title_observation',
        ]

    def clean(self):
        library_observation_form_validation(self, CreateLibraryObservationForm)
        return self.cleaned_data
