from django.urls import path
from . import views

urlpatterns = [
    path("list", views.request_list, name="request_list"),
    path("add/<int:test_id>/", views.add_request, name="add_request"),
    path("remove/<int:test_id>/", views.remove_request, name="remove_request"),
    path("favorite-list", views.favorite_list, name="favorite_list"),
    path("favorite-add/<int:test_id>/", views.favorite_add, name="favorite_add"),
    path("favorite-remove/<int:test_id>/", views.favorite_remove, name="favorite_remove"),
    path("set_add_to_cart/<int:set_id>/", views.set_add_to_cart, name="set_add_to_cart"),
    path('update-unit/', views.update_unit, name='update_unit'),
]