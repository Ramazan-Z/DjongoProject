from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from catalog import models


def home(request: WSGIRequest) -> HttpResponse:
    """Контроллер главной страницы"""
    products = models.Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/home.html", context=context)


def contacts(request: WSGIRequest) -> HttpResponse:
    """Контроллер страницы контактов"""
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, "catalog/contacts.html")


def product_detail(request: WSGIRequest, product_id: int) -> HttpResponse:
    """Контроллер страницы описания продукта"""
    products = models.Product.objects.all()
    product = models.Product.objects.get(id=product_id)

    index = list(products).index(product)
    last_product = products[index - 1] if index > 0 else None
    next_product = products[index + 1] if index < (len(products) - 1) else None

    context = {
        "last_product": last_product,
        "product": product,
        "next_product": next_product,
    }
    return render(request, "catalog/product_detail.html", context)
