from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.forms.models import ModelFormMetaclass
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog import models
from config.settings import CACH_ENABLED

from .forms import ProductForm, ProductModeratorForm


class ProductsListView(ListView):
    """Контроллер главной страницы"""

    model = models.Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self) -> Any:
        """Отображение только опубликованных товаров для обычных пользователей,
        и всех для модератора и админа"""

        if CACH_ENABLED:
            queryset = cache.get("queryset")
            if not queryset:
                queryset = super().get_queryset()
                cache.set("queryset", queryset, 5 * 60)
        else:
            queryset = super().get_queryset()

        user = self.request.user
        if user.has_perm("catalog.delete_product"):
            return queryset
        return queryset.filter(status=True)


@method_decorator(cache_page(5 * 60), name="dispatch")
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы создания товара"""

    model = models.Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """Установка текущего пользователя владельцем товара"""

        object = form.save()
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер страницы обновления товара"""

    model = models.Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self) -> ModelFormMetaclass:
        """Ограничение редактирования только владельцу и модератору"""

        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер страницы удаления товара"""

    model = models.Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ограничение удаления только владельцу и модератору"""

        response = super().get(request, *args, **kwargs)
        user = self.request.user
        if user == self.object.owner or user.has_perm("catalog.delete_product"):
            return response
        raise PermissionDenied


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов"""

    template_name = "catalog/contacts.html"

    @staticmethod
    def post(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Переопределение метода"""
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
