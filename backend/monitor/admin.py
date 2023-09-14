from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.System)
admin.site.register(models.SystemDataInstance)