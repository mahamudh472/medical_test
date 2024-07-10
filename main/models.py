from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    # def get_tests(self):
    #     return self.test_set.all()


class Service(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)
    iso_certificate_status = models.BooleanField(default=False)
    iso_certificate_symbol = models.CharField(max_length=100, blank=True, null=True)
    open_24_hours = models.BooleanField(default=False)
    open_days = models.CharField(max_length=100, blank=True, null=True, default='Mondday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Test(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    billing_code = models.CharField(max_length=100)
    tz_std_tariff = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=100)
    tat = models.CharField(max_length=100)
    tat_unit = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class TestSet(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tests = models.ManyToManyField(Test, related_name='tests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name