from django.views.generic import ListView

from blog import models


class BlogEntryListView(ListView):
    """Контроллер страницы со списком записей"""

    model = models.BlogEntry
    context_object_name = "blogentry"
