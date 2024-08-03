from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test, Organization, TestSet, Service
from .utils import data
from django.db.models import Q
import datetime
from django.core.paginator import Paginator
import googlemaps
from math import radians, sin, cos, sqrt, atan2


# Create your views here.

def home(request):
    tests = Test.objects.all().order_by('?')[:8]
    test_sets = TestSet.objects.all().order_by('?')[:8]
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
    paginator = Paginator(tests, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    total_items = tests.count()
    context = {
        'tests': page_obj,
        'total_items': total_items
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
    location = request.GET.get('location')
    if location:
        return search_service(request)
    query = request.GET.get('query')

    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(organization__name__icontains=query) &
        Q(location__icontains=location)
    )
    services = services.distinct()

    tests = Test.objects.filter(
        Q(name__icontains=query) |
        Q(billing_code__icontains=query) |
        Q(sample_type__icontains=query) |
        Q(organization__name__icontains=query)
    )

    tests = tests.distinct()
    paginator = Paginator(tests, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    total_item = tests.count()
    context = {
        'tests': page_obj,
        'services': services,
        'query': query,
        'location': location,
        'total_item': total_item,
    }
    return render(request, "main/search.html", context)


# Helper function to calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Compute differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def search_service(request):
    # Get query parameters
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')

    api_key = settings.GOOGLE_MAPS_API_KEY
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Initial filter by query
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(organization__name__icontains=query)
    )

    # Convert location to geocode (latitude and longitude)
    user_lat = None
    user_lng = None

    if location:
        try:
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                user_lat = geocode_result[0]['geometry']['location']['lat']
                user_lng = geocode_result[0]['geometry']['location']['lng']
        except Exception as e:
            print(f"Error converting user location to geocode: {e}")

    # Filter services within 10 km radius for 'near-me' option
    if request.GET.get('near-me') == "yes" and user_lat is not None and user_lng is not None:
        nearby_services = []

        for service in services:
            # Convert service location to geocode
            try:
                service_geocode = gmaps.geocode(service.location)
                if service_geocode:
                    service_lat = service_geocode[0]['geometry']['location']['lat']
                    service_lng = service_geocode[0]['geometry']['location']['lng']

                    # Calculate distance between user and service location
                    distance = calculate_distance(user_lat, user_lng, service_lat, service_lng)

                    if distance <= 10:
                        nearby_services.append(service.id)
            except Exception as e:
                print(f"Error converting service location to geocode: {e}")

        # Filter services to include only nearby services
        services = services.filter(id__in=nearby_services)

    if request.GET.get('workplace') == "yes":
        pass
    if request.GET.get('24hours') == "yes":
        services = services.filter(open_24_hours=True)
    if request.GET.get('iso-certified') == "yes":
        services = services.filter(iso_certificate_status=True)

    # Ensure distinct results
    services = services.distinct()

    context = {
        'services': services,
    }

    return render(request, "main/search_service.html", context)


def search_suggestions(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    # if category == 'service':
    #     return search_service_suggestions(request)
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


# def search_service_suggestions(request):
#     query = request.GET.get('query')
#     # print(Service.objects.filter(organization__name__icontains=query))
#     services = Service.objects.filter(
#         Q(name__icontains=query) |
#         Q(location__icontains=query) |
#         Q(organization__name__icontains=query)
#     )
#     services = services.distinct()[:5]
#     print(services)
#     # only list of names
#     services = [service.name for service in services]
#     return JsonResponse(services, safe=False)


def insert_test_data(request):
    return HttpResponse("Data inserted successfully")
