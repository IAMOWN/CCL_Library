from django.urls import path

from .views import (
    TagList,
    TagDetail,
    TagCreate,
    TagUpdate,
    TagDelete,
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
    LibraryRecordDetail,
    LibraryRecordCreate,
    LibraryRecordUpdate,
    LibraryRecordDelete,
    SearchView,
)

urlpatterns = [
    # Tags
    path('tags/', TagList.as_view(), name='tags'),
    path('tag/<int:pk>/', TagDetail.as_view(), name='tag'),
    path('tag_create/', TagCreate.as_view(), name='tag-create'),
    path('tag_update/<int:pk>/', TagUpdate.as_view(), name='tag-update'),
    path('tag_delete/<int:pk>/', TagDelete.as_view(), name='tag-delete'),

    # Discourse Series
    path('discourse_seriess/', DiscourseSeriesList.as_view(), name='discourse-series'),
    path('discourse_series/<int:pk>/', DiscourseSeriesDetail.as_view(), name='discourse-series-detail'),
    path('discourse_series_create/', DiscourseSeriesCreate.as_view(), name='discourse-series-create'),
    path('discourse_series_update/<int:pk>/', DiscourseSeriesUpdate.as_view(), name='discourse-series-update'),
    path('discourse_series_delete/<int:pk>/', DiscourseSeriesDelete.as_view(), name='discourse-series-delete'),

    # Authors
    path('authors/', CosmicAuthorList.as_view(), name='authors'),
    path('author/<int:pk>/', CosmicAuthorDetail.as_view(), name='author'),
    path('author_create/', CosmicAuthorCreate.as_view(), name='author-create'),
    path('author_update/<int:pk>/', CosmicAuthorUpdate.as_view(), name='author-update'),
    path('author_delete/<int:pk>/', CosmicAuthorDelete.as_view(), name='author-delete'),

    # Library Records
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

    # Search
    path('library_records/search/', SearchView.as_view(), name='search'),
]
