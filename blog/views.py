from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog import models


class BlogEntryListView(ListView):
    """Контроллер страницы со списком записей"""

    model = models.BlogEntry
    context_object_name = "blogentries"

    def get_queryset(self) -> QuerySet:
        """Переопределение метода"""
        query_set = super().get_queryset()
        return query_set.filter(is_publication=True)


class BlogEntryDetailView(DetailView):
    """Контроллер страницы с деталями записи"""

    model = models.BlogEntry
    context_object_name = "blogentry"

    def get_object(self, queryset: QuerySet[Any, Any] | None = None) -> Any:
        """Переопределение метода"""
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class BlogEntryCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы создания записи"""

    model = models.BlogEntry
    fields = ["heading", "content", "preview", "is_publication"]
    template_name = "blog/blogentry_form.html"
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер страницы обновления записи"""

    model = models.BlogEntry
    fields = ["heading", "content", "preview", "is_publication"]
    template_name = "blog/blogentry_form.html"
    context_object_name = "blogentry"
    success_url = reverse_lazy("blog:blogentry_list")

    def get_success_url(self) -> str:
        """Переопределение метода"""
        return reverse("blog:blogentry_detail", args=[self.kwargs.get("pk")])


class BlogEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.BlogEntry
    template_name = "blog/blogentry_confirm_delete.html"
    context_object_name = "blogentry"
    success_url = reverse_lazy("blog:blogentry_list")
