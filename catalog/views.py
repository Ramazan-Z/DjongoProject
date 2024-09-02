from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def home(request: WSGIRequest) -> HttpResponse:
    """Контроллер главной страницы"""
    return render(request, "catalog/home.html")


def contacts(request: WSGIRequest) -> HttpResponse:
    """Контроллер страницы контактов"""
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, "catalog/contacts.html")
