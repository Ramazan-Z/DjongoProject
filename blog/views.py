from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog import models


class BlogEntryListView(ListView):
    """Контроллер страницы со списком записей"""

    model = models.BlogEntry
    context_object_name = "blogentries"


class BlogEntryDetailView(DetailView):
    """Контроллер страницы с деталями записи"""

    model = models.BlogEntry
    context_object_name = "blogentry"


class BlogEntryCreateView(CreateView):
    """Контроллер страницы создания записи"""

    model = models.BlogEntry
    fields = ["heading", "content", "preview", "is_publication"]
    template_name = "blog/blogentry_form.html"
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryUpdateView(UpdateView):
    """Контроллер страницы обновления записи"""

    model = models.BlogEntry
    fields = ["heading", "content", "preview", "is_publication"]
    template_name = "blog/blogentry_form.html"
    context_object_name = "blogentry"
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryDeleteView(DeleteView):
    model = models.BlogEntry
    template_name = "blog/blogentry_confirm_delete.html"
    context_object_name = "blogentry"
    success_url = reverse_lazy("blog:blogentry_list")
