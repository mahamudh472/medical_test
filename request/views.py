from django.shortcuts import render, redirect
from main.models import Test, TestSet
from .models import Request, Favorite
from django.contrib import messages

# Create your views here.

def add_request(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.user.is_authenticated:
        req, created = Request.objects.get_or_create(user=request.user)
        req.tests.add(test)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        req, created = Request.objects.get_or_create(anynomous_user=key)
        req.tests.add(test)
        
    messages.success(request, "Test added to request")
    return redirect(request.META.get('HTTP_REFERER'))

def remove_request(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.user.is_authenticated:
        req = Request.objects.get(user=request.user)
        req.tests.remove(test)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        req = Request.objects.get(anynomous_user=key)
        req.tests.remove(test)
        
    messages.success(request, "Test removed from request")
    return redirect(request.META.get('HTTP_REFERER'))

def request_list(request):
    if request.user.is_authenticated:
        requests = Request.objects.filter(user=request.user).first()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        requests = Request.objects.filter(anynomous_user=key).first()
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
        if not key:
            request.session.create()
            key = request.session.session_key
        fav, created = Favorite.objects.get_or_create(anynomous_user=key)
        fav.tests.add(test)

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
        req, created = Request.objects.get_or_create(user=request.user)
        req.tests.add(*test_set.tests.all())
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        req, created = Request.objects.get_or_create(anynomous_user=key)
        req.tests.add(*test_set.tests.all())

    messages.success(request, "Test set added to request")
    return redirect(request.META.get('HTTP_REFERER'))













