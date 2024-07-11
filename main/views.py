from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test, Organization, TestSet, Service
from .utils import data
from django.db.models import Q
import datetime



# Create your views here.

def home(request):
    tests = Test.objects.all().order_by('?')[:12]
    test_sets = TestSet.objects.all().order_by('?')[:12]
    context = {
        'tests': tests,
        'test_sets': test_sets
    }
    return render(request, "main/home.html", context)


def organisation(request, id):
    org = Organization.objects.get(id=id)
    context = {
        'org': org
    }
    return render(request, "main/organisation.html", context)


def all_tests(request):
    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, "main/all_tests.html", context)


def all_test_sets(request):
    test_sets = TestSet.objects.all()
    context = {
        'test_sets': test_sets
    }
    return render(request, "main/all_test_sets.html", context)


def test_sets(request, id):
    test_set = TestSet.objects.get(id=id)
    context = {
        'test_set': test_set
    }
    return render(request, "main/test_sets.html", context)


def search(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    if category == 'service':
        return search_service(request)
    tests = Test.objects.filter(
        Q(name__icontains=query) |
        Q(billing_code__icontains=query) |
        Q(sample_type__icontains=query) |
        Q(organization__name__icontains=query)
    )
    tests = tests.distinct()
    context = {
        'tests': tests,
    }
    return render(request, "main/search.html", context)


def search_service(request):
    query = request.GET.get('query')
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(location__icontains=query) |
        Q(organization__name__icontains=query)
    )
    services = services.distinct()
    context = {
        'services': services,
    }
    return render(request, "main/search_service.html", context)


def search_suggestions(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    if category == 'service':
        return search_service_suggestions(request)
    tests = Test.objects.filter(
        Q(name__icontains=query) |
        Q(billing_code__icontains=query) |
        Q(sample_type__icontains=query) |
        Q(organization__name__icontains=query) 
    )
    tests = tests.distinct()[:5]
    # only list of names
    tests = [test.name for test in tests]
    return JsonResponse(tests, safe=False)


def search_service_suggestions(request):
    query = request.GET.get('query')
    # print(Service.objects.filter(organization__name__icontains=query))
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(location__icontains=query) |
        Q(organization__name__icontains=query)
    )
    services = services.distinct()[:5]
    print(services)
    # only list of names
    services = [service.name for service in services]
    return JsonResponse(services, safe=False)
    








def insert_test_data(request):

    return HttpResponse("Data inserted successfully")