from .models import Request

def request_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Request.objects.filter(user=request.user).first()
        if count:
            count = count.tests.count()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        count = Request.objects.filter(anynomous_user=key).first()
        if count:
            count = count.tests.count()

    return {"request_count": count}