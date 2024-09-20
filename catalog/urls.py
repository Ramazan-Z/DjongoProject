from django.urls import path

from catalog.apps import CatalogConfig

from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("product_detail/<int:product_id>", views.product_detail, name="product_detail"),
]
