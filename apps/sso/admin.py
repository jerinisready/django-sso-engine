from django.contrib import admin

from apps.sso.models import Client, Feature

# Register your models here.

admin.site.register(Client)
admin.site.register(Feature)
