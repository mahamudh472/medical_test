from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("organisation/<int:id>/", views.organisation, name="organisation"),
    path("all-tests/", views.all_tests, name="all_tests"),
    path("all-test-sets/", views.all_test_sets, name="all_test_sets"),
    path("test-sets/<int:id>/", views.test_sets, name="test_sets"),
    path("search/", views.search_service, name="search"),
    path("suggestions/", views.search_suggestions, name="search_suggestions"),
    path("insert_test_data/", views.insert_test_data, name="insert_test_data"),
]