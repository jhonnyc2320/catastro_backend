from django.contrib import admin
from django.apps import apps
from .models import *

# Register your models here.
app = apps.get_app_config('dominios')

for model_name, model in app.models.items():
    admin_class = type('AdminClass', (admin.ModelAdmin,), {})
    admin.site.register(model, admin_class)