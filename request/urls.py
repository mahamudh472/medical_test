from django.urls import path
from . import views

urlpatterns = [
    path("list", views.request_list, name="request_list"),
    path("add/<int:test_id>/", views.add_request, name="add_request"),
    path("remove/<int:test_id>/", views.remove_request, name="remove_request"),
]