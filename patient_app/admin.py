from django.contrib import admin

# Register your models here.

from .models import Patient


admin.site.register(Patient)
# admin.site.register(Constant)
# admin.site.register(Receipt)