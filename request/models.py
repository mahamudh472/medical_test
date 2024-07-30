from django.db import models
from django.contrib.auth.models import User
from main.models import Test, Service


# Create your models here.

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anynomous_user = models.CharField(max_length=200, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    unit = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_sub_total(self):
        sub_total = 0
        if self.user:
            for obj in self.user.request_set.all():
                sub_total += obj.unit * obj.test.tz_std_tariff
        else:
            for obj in Request.objects.filter(anynomous_user=self.anynomous_user):
                sub_total += obj.unit * obj.test.tz_std_tariff
        return "{:.2f}".format(sub_total)

    def get_price(self):
        return self.unit * self.test.tz_std_tariff


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anynomous_user = models.CharField(max_length=200, null=True, blank=True)
    tests = models.ManyToManyField(Test, related_name='favorite_tests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



STATUS_CHOICES = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('CANCELLED', 'CANCELLED'),
)


class Order(models.Model):
    alphanumeric_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    requests = models.ManyToManyField(Request, related_name='order_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    # Insurance
    insurance_membership_id = models.CharField(max_length=50, null=True, blank=True)
    insurance_expiry_date = models.DateField(null=True, blank=True)
    # Collection Site 
    collection_center = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    collection_home = models.TextField(null=True, blank=True)
    collection_distance = models.CharField(max_length=200, null=True, blank=True)
    collection_fee = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alphanumeric_id
