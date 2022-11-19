from django.contrib import admin

from .models import User, Report
# Register your models here.
admin.site.register(Report)
admin.site.register(User)
