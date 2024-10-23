from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
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

from .forms import ProductForm, ProductModeratorForm
from .services import CategoriesServices, ProductServices


class ProductsListView(ListView):
    """Контроллер главной страницы"""

    model = models.Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self) -> Any:
        """Кэширование и проверка прав пользователя"""
        queryset = super().get_queryset()
        queryset = ProductServices.check_cache(queryset)
        # Проверка прав пользователя
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
    return_url = reverse_lazy("catalog:home")  # URL для кнопки "Назад"

    def get_context_data(self, **kwargs: Any) -> dict[str, QuerySet]:
        """Передача в шаблон URL для кнопки «Назад»"""
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.return_url
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Установка URL для кнопки «Назад», если указано в запросе"""
        return_url_marker = request.GET.get("return")
        if return_url_marker:
            self.return_url = reverse_lazy("catalog:categories")
        return super().get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы создания товара"""

    model = models.Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """Установка текущего пользователя владельцем товара"""
        product = form.save()
        product.owner = self.request.user
        product.save()
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
        """Простой ответ на POST запрос"""
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class CategoriesTemplateView(TemplateView):
    """Контроллер страницы категорий"""

    model = models.Product
    template_name = "catalog/categories.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs: Any) -> dict[str, QuerySet]:
        """Передача в шаблон списка категорий, текущей категории и набора товаров"""
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoriesServices.get_categories()
        context["current_category"] = CategoriesServices.get_current_category()
        context[self.context_object_name] = CategoriesServices.get_queryset()
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обработка запроса выбора категории для отображения"""
        category_name = request.POST.get("category")
        CategoriesServices.set_current_category(category_name)
        return super().get(request, *args, **kwargs)
