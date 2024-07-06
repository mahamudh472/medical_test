from .models import Request

def request_count(request):
    if request.user.is_authenticated:
        count = Request.objects.filter(user=request.user).first().tests.count()
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        count = Request.objects.filter(anynomous_user=key).first().tests.count()
    return {"request_count": count}