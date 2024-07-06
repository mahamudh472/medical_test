
from .models import Test, Organization, TestSet, Service

def orgs(request):
    orgs = Organization.objects.all()[:50]
    return {'orgs': orgs}