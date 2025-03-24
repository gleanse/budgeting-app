from django.contrib import admin

# Register your models here.

# NOTE: temporary models only subject to delete after set up
from .models import Budget
admin.site.register(Budget)