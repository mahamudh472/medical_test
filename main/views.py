from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test, Organization, TestSet, Service
from .utils import data
from django.db.models import Q



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
    tests = Test.objects.filter(
        Q(name__icontains=query) |
        Q(billing_code__icontains=query) |
        Q(sample_type__icontains=query)
    )
    tests = tests.distinct()
    context = {
        'tests': tests,
    }
    return render(request, "main/search.html", context)


def search_suggestions(request):
    query = request.GET.get('query')
    tests = Test.objects.filter(
        Q(name__icontains=query) |
        Q(billing_code__icontains=query) |
        Q(sample_type__icontains=query)
    )
    tests = tests.distinct()[:5]
    # only list of names
    tests = [test.name for test in tests]
    return JsonResponse(tests, safe=False)
    

















def insert_test_data(request):
    for test in data:
        test_obj = Test.objects.create(
            name=test['TEST DESCRIPTION'],
            billing_code=test['BILLING CODE'],
            tz_std_tariff=test['TZ STD TARRIF'],
            sample_type=test['SMPLE TYPE'],
            tat=test['TAT'],
            tat_unit=test['TAT UNIT']
        )