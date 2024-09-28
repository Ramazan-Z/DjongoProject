from django.urls import path

from blog.apps import BlogConfig

from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("blogentry_list/", views.BlogEntryListView.as_view(), name="blogentry_list"),
    path("blogentry_detail/<int:pk>/", views.BlogEntryDetailView.as_view(), name="blogentry_detail"),
    path("blogentry/new/", views.BlogEntryCreateView.as_view(), name="blogentry_new"),
    path("blogentry/<int:pk>/edit/", views.BlogEntryUpdateView.as_view(), name="blogentry_edit"),
    path("blogentry/<int:pk>/delete/", views.BlogEntryDeleteView.as_view(), name="blogentry_delete"),
]
