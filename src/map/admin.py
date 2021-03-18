from django.contrib import admin
from .models import Map, ReportedImages

# Register models for use on dev
admin.site.register(Map)
admin.site.register(ReportedImages)