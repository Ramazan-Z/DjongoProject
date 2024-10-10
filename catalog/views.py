from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog import models

from .forms import ProductForm


class ProductsListView(ListView):
    """Контроллер главной страницы"""

    model = models.Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    """Контроллер страницы описания товара"""

    model = models.Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs: Any) -> dict[str, QuerySet]:
        """Переопределение метода"""
        context = super().get_context_data(**kwargs)
        products = self.model.objects.all()
        index = list(products).index(context["product"])
        context["last_product"] = products[index - 1] if index > 0 else None
        context["next_product"] = products[index + 1] if index < (len(products) - 1) else None
        return context


class ProductCreateView(CreateView):
    """Контроллер страницы создания товара"""

    model = models.Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    """Контроллер страницы обновления товара"""

    model = models.Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(DeleteView):
    """Контроллер страницы удаления товара"""

    model = models.Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов"""

    template_name = "catalog/contacts.html"

    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Переопределение метода"""
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
