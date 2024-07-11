from .models import Request, Favorite

def request_count(request):
    count = 0
    favorite_count = 0
    if request.user.is_authenticated:
        count2 = Request.objects.filter(user=request.user).first()
        favorite_count2 = Favorite.objects.filter(user=request.user).first()
        if count2: count = count2.tests.count()
        if favorite_count2: favorite_count = favorite_count2.tests.count()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        count2 = Request.objects.filter(anynomous_user=key).first()
        favorite_count2 = Favorite.objects.filter(anynomous_user=key).first()
        if count2: count = count2.tests.count()
        if favorite_count2: favorite_count = favorite_count2.tests.count()

    return {"request_count": count, "favorite_count": favorite_count}