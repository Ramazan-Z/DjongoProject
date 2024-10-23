from django.urls import path

from catalog.apps import CatalogConfig

from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.ProductsListView.as_view(), name="home"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product_new/", views.ProductCreateView.as_view(), name="product_new"),
    path("product_edit/<int:pk>/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("product_delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product_confirm_delete"),
    path("contacts/", views.ContactsTemplateView.as_view(), name="contacts"),
    path("categories/", views.CategoriesTemplateView.as_view(), name="categories"),
]
