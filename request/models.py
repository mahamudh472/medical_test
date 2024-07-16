from django.db import models
from django.contrib.auth.models import User
from main.models import Test, TestSet

# Create your models here.

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anynomous_user = models.CharField(max_length=200, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
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
        return sub_total

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