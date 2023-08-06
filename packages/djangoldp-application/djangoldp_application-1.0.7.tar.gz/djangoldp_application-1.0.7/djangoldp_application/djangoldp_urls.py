from django.urls import path
from .views import ApplicationViewSet, ApplicationDetailViewSet

urlpatterns = [
    path(
        "ansible/inventory/",
        ApplicationViewSet.as_view({"get": "list"}),
        name="ansible_inventory",
    ),
    path(
        "ansible/<slug:slug>/",
        ApplicationDetailViewSet.as_view({"get": "retrieve"}, lookup_field="slug"),
        name="ansible_inventory_detail",
    ),
]
