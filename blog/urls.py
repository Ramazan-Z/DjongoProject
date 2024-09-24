from django.urls import path

from blog.apps import BlogConfig

from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("blogentry_list/", views.BlogEntryListView.as_view(), name="blogentry_list"),
]
