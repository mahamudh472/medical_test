from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Test, TestSet, Service
from .models import Request, Favorite, Order
from django.contrib import messages
from django.views.decorators.http import require_POST
import stripe
from django.conf import settings
import requests
import random
import googlemaps

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def add_request(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.user.is_authenticated:
        req = Request.objects.get_or_create(user=request.user, test=test)
        req[0].save()

    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        req = Request.objects.get_or_create(anynomous_user=key, test=test)
        req[0].save()

    messages.success(request, "Test added to request")
    return redirect(request.META.get('HTTP_REFERER'))


def remove_request(request, test_id):
    req = Request.objects.filter(id=test_id)
    if req.exists():
        req[0].delete()

    messages.success(request, "Test removed from request")
    return redirect(request.META.get('HTTP_REFERER'))


def request_list(request):
    if request.user.is_authenticated:
        requests = Request.objects.filter(user=request.user)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        requests = Request.objects.filter(anynomous_user=key)
    context = {
        'request': requests
    }
    return render(request, "request/request_list.html", context)


def favorite_add(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.user.is_authenticated:
        fav, created = Favorite.objects.get_or_create(user=request.user)
        fav.tests.add(test)
    else:
        key = request.session.session_key
        print(key)
        if not key:
            request.session.create()
            key = request.session.session_key
        fav, created = Favorite.objects.get_or_create(anynomous_user=key)
        fav.tests.add(test)
        print("working")

    messages.success(request, "Test added to favorite")
    return redirect(request.META.get('HTTP_REFERER'))


def favorite_remove(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.user.is_authenticated:
        fav = Favorite.objects.get(user=request.user)
        fav.tests.remove(test)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        fav = Favorite.objects.get(anynomous_user=key)
        fav.tests.remove(test)

    messages.success(request, "Test removed from favorite")
    return redirect(request.META.get('HTTP_REFERER'))


def favorite_list(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).first()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        favorites = Favorite.objects.filter(anynomous_user=key).first()
    tests = favorites.tests.all() if favorites else []
    context = {
        'tests': tests
    }
    return render(request, "request/favorite_list.html", context)


def set_add_to_cart(request, set_id):
    test_set = TestSet.objects.get(id=set_id)
    if request.user.is_authenticated:
        for test in test_set.tests.all():
            req = Request.objects.get_or_create(user=request.user, test=test)
            req[0].save()

    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        for test in test_set.tests.all():
            req = Request.objects.get_or_create(anynomous_user=key, test=test)
            req[0].save()

    messages.success(request, "Test set added to request")
    return redirect(request.META.get('HTTP_REFERER'))


@require_POST
def update_unit(request):
    req_id = request.POST.get('test_id')
    unit = int(request.POST.get('unit'))

    # Find the test object and update the unit
    req = get_object_or_404(Request, id=req_id)
    req.unit = unit
    req.save()
    if req.unit == 0:
        req.delete()
        return JsonResponse({'success': True})

    # Calculate the new amount
    new_amount = req.unit * req.test.tz_std_tariff

    return JsonResponse({'success': True, 'new_unit': req.unit, 'new_amount': new_amount})


def checkout(request):
    if request.user.is_authenticated:
        requests = Request.objects.filter(user=request.user)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        requests = Request.objects.filter(anynomous_user=key)
    services = Service.objects.all()
    context = {
        'request': requests,
        'service': services
    }
    return render(request, "request/place-order.html", context)


def calculate_delivery_fee(request):
    if request.method == 'POST':
        # Extract data from POST request
        address = request.POST.get('address')
        delivery_type = request.POST.get('delivery_type')
        service_location = request.POST.get('service_location')
        api_key = settings.GOOGLE_MAPS_API_KEY
        print(address)
        print(delivery_type)
        print(service_location)
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)

        try:
            # Call Google Maps API for distance calculation
            response = gmaps.distance_matrix(
                origins=service_location,
                destinations=address,
                mode="driving"
            )

            # Extract distance
            distance_meters = response['rows'][0]['elements'][0]['distance']['value']

            # Get the service details from the database
            service = Service.objects.get(location=service_location)

            # Calculate delivery fee based on the delivery type
            if delivery_type == "standard":
                delivery_fee = (distance_meters / 1000) * service.organization.cost_per_km + 1000
            else:
                delivery_fee = (distance_meters / 1000) * service.organization.cost_per_km + 5000

            # Return JSON response
            return JsonResponse({'delivery_fee': f"{delivery_fee:.2f}", "distance": (distance_meters / 1000)})
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return JsonResponse({'error': 'Unable to calculate delivery fee. Please try again later.'})

    return JsonResponse({'error': 'Invalid request method.'})


def CreateStripeCheckoutSessionView(request):
    if request.method == 'POST':
        price = float(request.POST.get('price'))
        alphanumeric_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))

        # Add 18% tax with total price
        price += price * .18
        # check the mobile number
        mobile = str(request.POST.get('mobile'))
        if not mobile.startswith("+255"):
            mobile = "+255" + mobile

        order = Order.objects.create(
            alphanumeric_id=alphanumeric_id,
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            email=request.POST.get('email'),
            mobile=mobile,
            address='test'  # if user select collection center, save the center address
        )
        collection = request.POST.get('delivery-option')
        if str(collection) == "collection-center":
            location = request.POST.get('collection-center')
            center = Service.objects.get(location=location)
            order.collection_center = center
        elif str(collection) == "collection-home":
            address = request.POST.get('address')
            order.address = address
            delivery_fee = request.POST.get('delivery_fee')
            price += float(delivery_fee)

        insurance = request.POST.get('insurance_status')
        if insurance == "yes":
            order.insurance_membership_id = request.POST.get('insurance-id')
            order.insurance_expiry_date = request.POST.get('expiry-date')
            return redirect('success', alphanumeric_id)
        order.save()

        domain_url = request.headers['Referer'].split('/request')[0]
        print(domain_url)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/request/success/' + alphanumeric_id,
                cancel_url=domain_url + '/request/cancel/' + alphanumeric_id,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'tzs',
                            'unit_amount': int(float(price) * 100),
                            'product_data': {
                                'name': 'Cloud Script Order',
                            },
                        },
                        'quantity': 1,
                    }
                ],
                metadata={
                    'order_id': order.id,  # pass order ID here
                }
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request'})


def success(request, alphanumeric_id):
    # make order complete, remove cart items
    order = Order.objects.get(alphanumeric_id=alphanumeric_id)
    order.status = "COMPLETED"
    order.save()
    if request.user.is_authenticated:
        req = Request.objects.filter(user=request.user)
        req.delete()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        req = Request.objects.filter(anynomous_user=key)
        req.delete()

    return render(request, 'request/success.html')


def cancelled(request, alphanumeric_id):
    # make order canceled
    order = Order.objects.get(alphanumeric_id=alphanumeric_id)
    order.status = "CANCELLED"
    order.save()
    return render(request, 'request/cancel.html')
