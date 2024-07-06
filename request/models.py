from django.db import models
from django.contrib.auth.models import User
from main.models import Test, TestSet

# Create your models here.

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anynomous_user = models.CharField(max_length=200, null=True, blank=True)
    tests = models.ManyToManyField(Test, related_name='request_tests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username