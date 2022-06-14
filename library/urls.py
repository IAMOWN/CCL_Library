from django.urls import path

from .views import (
    TagList,
    TagDetail,
    TagCreate,
    TagUpdate,
    TagDelete,
    CollectionList,
    CollectionDetail,
    CollectionCreate,
    CollectionUpdate,
    CollectionDelete,
    DiscourseSeriesList,
    DiscourseSeriesDetail,
    DiscourseSeriesCreate,
    DiscourseSeriesUpdate,
    DiscourseSeriesDelete,
    CosmicAuthorList,
    CosmicAuthorDetail,
    CosmicAuthorCreate,
    CosmicAuthorUpdate,
    CosmicAuthorDelete,
    LibraryRecordList,
    BooksList,
    CosmicReviewsList,
    DiscoursesList,
    InvocationsList,
    PetitionsList,
    SeriesBootCampList,
    LibraryRecordDetail,
    LibraryRecordCreate,
    LibraryRecordUpdate,
    LibraryRecordDelete,
    SearchView,
    collection_records,
    collection_record_update,
    collection_record_delete,
    collection_record_detail,
    collection_record_form,

    CollectionENACAList,
    CollectionGESARAList,
    CollectionIAMFreedomList,
)

urlpatterns = [
    # Tags
    path('tags/', TagList.as_view(), name='tags'),
    path('tag/<int:pk>/', TagDetail.as_view(), name='tag'),
    path('tag_create/', TagCreate.as_view(), name='tag-create'),
    path('tag_update/<int:pk>/', TagUpdate.as_view(), name='tag-update'),
    path('tag_delete/<int:pk>/', TagDelete.as_view(), name='tag-delete'),

    # Collections
    path('collections/', CollectionList.as_view(), name='collections'),
    path('collection/<int:pk>/', CollectionDetail.as_view(), name='collection'),
    path('collection_create/', CollectionCreate.as_view(), name='collection-create'),
    path('collection_update/<int:pk>/', CollectionUpdate.as_view(), name='collection-update'),
    path('collection_delete/<int:pk>/', CollectionDelete.as_view(), name='collection-delete'),

    # Discourse Series
    path('discourse_seriess/', DiscourseSeriesList.as_view(), name='discourse-series'),
    path('discourse_series/<int:pk>/', DiscourseSeriesDetail.as_view(), name='discourse-series-detail'),
    path('discourse_series_create/', DiscourseSeriesCreate.as_view(), name='discourse-series-create'),
    path('discourse_series_update/<int:pk>/', DiscourseSeriesUpdate.as_view(), name='discourse-series-update'),
    path('discourse_series_delete/<int:pk>/', DiscourseSeriesDelete.as_view(), name='discourse-series-delete'),

    # Masters
    path('masters/', CosmicAuthorList.as_view(), name='masters'),
    path('master/<int:pk>/', CosmicAuthorDetail.as_view(), name='master'),
    path('master_create/', CosmicAuthorCreate.as_view(), name='master-create'),
    path('master_update/<int:pk>/', CosmicAuthorUpdate.as_view(), name='master-update'),
    path('master_delete/<int:pk>/', CosmicAuthorDelete.as_view(), name='master-delete'),

    # Library Records
    path('library_records/', LibraryRecordList.as_view(), name='library-records'),
    path('library_records/', LibraryRecordList.as_view(), name='library-records'),
    path('library_records/books/', BooksList.as_view(), name='books'),
    path('library_records/cosmic_reviews/', CosmicReviewsList.as_view(), name='cosmic-reviews'),
    path('library_records/discourses/', DiscoursesList.as_view(), name='discourses'),
    path('library_records/invocations/', InvocationsList.as_view(), name='invocations'),
    path('library_records/petitions/', PetitionsList.as_view(), name='petitions'),
    path('library_record/<int:pk>/', LibraryRecordDetail.as_view(), name='library-record'),
    path('library_record_create/', LibraryRecordCreate.as_view(), name='library-record-create'),
    path('library_record_update/<int:pk>/', LibraryRecordUpdate.as_view(), name='library-record-update'),
    path('library_record_delete/<int:pk>/', LibraryRecordDelete.as_view(), name='library-record-delete'),

    # Library Record Series
    path('library_record/series/boot_camp/', SeriesBootCampList.as_view(), name='boot-camp'),

    # Library Record Collections
    path('library_record/collection/enaca/', CollectionENACAList.as_view(), name='enaca'),
    path('library_record/collection/gesara/', CollectionGESARAList.as_view(), name='gesara'),
    path('library_record/collection/IAMFreedom/', CollectionIAMFreedomList.as_view(), name='i-am-freedom'),

    # Search
    path('library_records/search/', SearchView.as_view(), name='search'),

    # Collection Records
    path('collection_records/<pk>/', collection_records, name='collection-records'),
    path('htmx/collection_record_form/', collection_record_form, name='collection-record-form'),
    path('htmx/collection_record/<pk>/', collection_record_detail, name='collection-record-detail'),
    path('htmx/collection_record/<pk>/delete/', collection_record_delete, name='collection-record-delete'),
    path('htmx/collection_record/<pk>/update/', collection_record_update, name='collection-record-update'),
]
