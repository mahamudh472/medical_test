from django.contrib import admin
from .models import Organization, Service, Test, TestSet

# Register your models here.
"""
Show the associated Service and Test objects in the Organization admin page
"""
class ServiceInline(admin.StackedInline ):
    model = Service
    extra = 1

class TestInline(admin.StackedInline ):
    model = Test
    extra = 1

class TestSetInline(admin.StackedInline ):
    model = TestSet
    extra = 1
    filter_horizontal = ('tests',)

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [ServiceInline, TestInline, TestSetInline]
    list_display = ('name', 'admin', 'updated_at')
    search_fields = ['name']

admin.site.register(Organization, OrganizationAdmin)


class TestSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'updated_at')
    search_fields = ['name']
    filter_horizontal = ('tests',)

admin.site.register(TestSet, TestSetAdmin)

admin.site.register(Service)
admin.site.register(Test)


